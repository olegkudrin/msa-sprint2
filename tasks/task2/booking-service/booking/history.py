import logging
import socket

import orjson
from confluent_kafka import KafkaError, Message, Producer

from .models import Booking
from .options import config


class HistoryProducer:
    def __init__(self):
        conf = {
            "bootstrap.servers": config.kafka.bootstrap_servers,
            "client.id": socket.gethostname(),
        }
        self._producer = Producer(conf)
        self._topic = config.kafka.history_topic

    def _acked(self, err: KafkaError | None, msg: Message):
        if err is not None:
            logging.error(f"% Message failed delivery: {err}\n")
        else:
            logging.info(
                f"% Message delivered to {msg.topic()} "
                f"[{msg.partition()}] @ {msg.offset()}\n"
            )

    def produce(self, booking: Booking):
        try:
            self._producer.produce(
                self._topic,
                orjson.dumps(booking.to_dict()),
                callback=self._acked,
            )
        except BufferError:
            logging.warning(
                f"% Local producer queue is full ({len(self._producer)} "
                "messages awaiting delivery): try again\n"
            )
        self._producer.poll(0.0)

    def flush(self):
        logging.info(f"% Waiting for {len(self._producer)} deliveries\n")
        self._producer.flush()
