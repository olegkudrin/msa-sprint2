import logging
import signal
import sys
from concurrent import futures

import booking_pb2
import booking_pb2_grpc
import grpc
from sqlalchemy import select

from . import proxy
from .database import create_tables, get_session
from .history import HistoryProducer
from .models import Booking
from .options import config


class BookingService(booking_pb2_grpc.BookingServiceServicer):
    def __init__(self, history_producer: HistoryProducer):
        self._history_producer = history_producer

    def ListBookings(self, request, context):
        stmt = select(Booking).order_by(Booking.created_at)
        if request.user_id is not None:
            stmt = stmt.where(Booking.user_id == request.user_id)

        with get_session() as session:
            result = session.execute(stmt)
            response = booking_pb2.BookingListResponse()
            for booking in result.scalars():
                item = self._make_booking_pb2(booking)
                response.bookings.append(item)

        return response

    def CreateBooking(self, request, context):
        logging.info(
            f"Creating booking: user_id={request.user_id}, "
            f"hotel_id={request.hotel_id}, promo_code={request.promo_code}"
        )

        self._validate_user(request.user_id)
        self._validate_hotel(request.hotel_id)

        base_price = self._resolve_base_price(request.user_id)
        discount = self._resolve_promo_discount(request.promo_code, request.user_id)

        final_price = base_price - discount
        logging.info(
            f"Final price calculated: base={base_price}, "
            f"discount={discount}, final={final_price}"
        )

        with get_session() as session:
            booking = Booking(
                user_id=request.user_id,
                hotel_id=request.hotel_id,
                promo_code=request.promo_code,
                discount_percent=discount,
                price=final_price,
            )
            session.add(booking)
            session.commit()
            response = self._make_booking_pb2(booking)

        self._history_producer.produce(booking)

        return response

    def _make_booking_pb2(self, booking):
        return booking_pb2.BookingResponse(
            id=str(booking.id),
            user_id=booking.user_id,
            hotel_id=booking.hotel_id,
            promo_code=booking.promo_code,
            discount_percent=booking.discount_percent,
            price=booking.price,
            created_at=booking.created_at.isoformat(),
        )

    def _validate_user(self, user_id):
        if not proxy.is_user_active(user_id):
            logging.warning(f"User {user_id} is inactive")
            raise Exception("User is inactive")

        if proxy.is_user_blacklisted(user_id):
            logging.warning(f"User {user_id} is blacklisted")
            raise Exception("User is blacklisted")

    def _validate_hotel(self, hotel_id):
        if not proxy.is_hotel_operational(hotel_id):
            logging.warning(f"Hotel {hotel_id} is not operational")
            raise Exception("Hotel is not operational")

        if not proxy.is_trusted_hotel(hotel_id):
            logging.warning(f"Hotel {hotel_id} is not trusted")
            raise Exception("Hotel is not trusted")

        if proxy.is_hotel_fully_booked(hotel_id):
            logging.warning(f"Hotel {hotel_id} is fully booked")
            raise Exception("Hotel is fully booked")

    def _resolve_base_price(self, user_id):
        status: str | None = proxy.get_user_status(user_id)
        if status:
            if status.upper() == "VIP":
                base_price = 80.0
            else:
                base_price = 100.0
            logging.debug(
                f"User {user_id} has status '{status}', base price is {base_price}"
            )
        else:
            base_price = 100.0
            logging.debug(
                f"User {user_id} has unknown status, default base price {base_price}"
            )
        return base_price

    def _resolve_promo_discount(self, promo_code, user_id):
        if not promo_code:
            return 0.0

        promo = proxy.validate_promo(promo_code, user_id)
        if not promo:
            logging.info(
                f"Promo code '{promo_code}' is invalid or not applicable for user {user_id}"
            )
            return 0.0

        discount = promo.discount
        logging.debug(f"Promo code '{promo_code}' applied with discount {discount}")
        return discount


def serve():
    history_producer = HistoryProducer()
    booking_service = BookingService(history_producer)

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    booking_pb2_grpc.add_BookingServiceServicer_to_server(booking_service, server)
    server.add_insecure_port(f"[::]:{config.service_port}")
    server.start()
    logging.info(f"Server started, listening on {config.service_port}")

    def signal_handler(signum, _frame):
        logging.info(f"Received signal {signum}, shutting down.")
        server.stop(grace=5)
        sys.exit(0)

    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)

    try:
        server.wait_for_termination()
    finally:
        history_producer.flush()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    create_tables()
    serve()
