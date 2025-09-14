from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class BookingRequest(_message.Message):
    __slots__ = ("user_id", "hotel_id", "promo_code")
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    HOTEL_ID_FIELD_NUMBER: _ClassVar[int]
    PROMO_CODE_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    hotel_id: str
    promo_code: str
    def __init__(self, user_id: _Optional[str] = ..., hotel_id: _Optional[str] = ..., promo_code: _Optional[str] = ...) -> None: ...

class BookingResponse(_message.Message):
    __slots__ = ("id", "user_id", "hotel_id", "promo_code", "discount_percent", "price", "created_at")
    ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    HOTEL_ID_FIELD_NUMBER: _ClassVar[int]
    PROMO_CODE_FIELD_NUMBER: _ClassVar[int]
    DISCOUNT_PERCENT_FIELD_NUMBER: _ClassVar[int]
    PRICE_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    id: str
    user_id: str
    hotel_id: str
    promo_code: str
    discount_percent: float
    price: float
    created_at: str
    def __init__(self, id: _Optional[str] = ..., user_id: _Optional[str] = ..., hotel_id: _Optional[str] = ..., promo_code: _Optional[str] = ..., discount_percent: _Optional[float] = ..., price: _Optional[float] = ..., created_at: _Optional[str] = ...) -> None: ...

class BookingListRequest(_message.Message):
    __slots__ = ("user_id",)
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    def __init__(self, user_id: _Optional[str] = ...) -> None: ...

class BookingListResponse(_message.Message):
    __slots__ = ("bookings",)
    BOOKINGS_FIELD_NUMBER: _ClassVar[int]
    bookings: _containers.RepeatedCompositeFieldContainer[BookingResponse]
    def __init__(self, bookings: _Optional[_Iterable[_Union[BookingResponse, _Mapping]]] = ...) -> None: ...
