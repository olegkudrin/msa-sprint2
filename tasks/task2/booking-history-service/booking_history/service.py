import logging
from signal import SIGINT, SIGTERM, signal

import orjson
from confluent_kafka import Consumer, KafkaError, KafkaException, Message
from confluent_kafka.admin import AdminClient, NewTopic
from orjson import JSONDecodeError

from .database import create_tables, get_session
from .models import BookingHistRec
from .options import config

running = True


def shutdown(_signum, _frame):
    global running
    running = False


def msg_process(msg: Message):
    logging.info(
        f"% {msg.topic()} [{msg.partition()}] "
        f"at offset {msg.offset()} with key {msg.key()}:\n"
    )
    logging.info(msg.value())

    try:
        value = msg.value()
        assert value is not None
        data = orjson.loads(value)
    except JSONDecodeError as e:
        logging.error(f"JSON decode error: {e}")
        return

    try:
        booking_hist_rec = BookingHistRec(
            booking_id=data["id"],
            user_id=data["user_id"],
            hotel_id=data["hotel_id"],
            price=data["price"],
            created_at=data["created_at"],
        )
    except Exception as e:
        logging.error(f"Creating history record error: {e}")
        return

    with get_session() as session:
        session.add(booking_hist_rec)
        session.commit()


def consume_loop(consumer: Consumer, topics: list[str]):
    try:
        consumer.subscribe(topics)

        while running:
            msg = consumer.poll(timeout=1.0)
            if msg is None:
                continue

            if err := msg.error():
                if err.code() == KafkaError._PARTITION_EOF:
                    logging.info(
                        f"% {msg.topic()} [{msg.partition()}] "
                        f"reached end at offset {msg.offset()}\n"
                    )
                else:
                    raise KafkaException(err)
            else:
                msg_process(msg)
                consumer.store_offsets(msg)
    finally:
        consumer.close()


def create_consumer():
    conf = {
        "bootstrap.servers": config.kafka.bootstrap_servers,
        "group.id": config.kafka.group_id,
        "auto.offset.reset": "earliest",
        "enable.auto.commit": True,
        "enable.auto.offset.store": False,
    }
    return Consumer(conf)


def create_admin():
    conf = {
        "bootstrap.servers": config.kafka.bootstrap_servers,
    }
    return AdminClient(conf)


def create_topics(admin, topics):
    admin = create_admin()
    new_topics = [NewTopic(topic) for topic in topics]
    fs = admin.create_topics(new_topics)

    for topic, f in fs.items():
        try:
            f.result()
            logging.info(f"Topic {topic} created")
        except KafkaException as e:
            err = e.args[0]
            assert isinstance(err, KafkaError)
            if err.code() != KafkaError.TOPIC_ALREADY_EXISTS:
                logging.info(f"Failed to create topic {topic}: {e}")


def serve():
    signal(SIGINT, shutdown)
    signal(SIGTERM, shutdown)

    admin = create_admin()
    create_topics(admin, [config.kafka.history_topic])

    consumer = create_consumer()
    consume_loop(consumer, [config.kafka.history_topic])


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    create_tables()
    serve()
