from datetime import date

import requests
from pydantic import BaseModel, ConfigDict, alias_generators

from .options import config

BASE_URL = config.monolith.url


def is_user_active(user_id: str) -> bool:
    r = requests.get(f"{BASE_URL}/api/users/{user_id}/active")
    assert r.status_code == 200
    return r.text == "true"


def is_user_blacklisted(user_id: str) -> bool:
    r = requests.get(f"{BASE_URL}/api/users/{user_id}/blacklisted")
    assert r.status_code == 200
    return r.text == "true"


def is_hotel_operational(hotel_id: str) -> bool:
    r = requests.get(f"{BASE_URL}/api/hotels/{hotel_id}/operational")
    assert r.status_code == 200
    return r.text == "true"


def is_trusted_hotel(hotel_id: str) -> bool:
    r = requests.get(f"{BASE_URL}/api/reviews/hotel/{hotel_id}/trusted")
    assert r.status_code == 200
    return r.text == "true"


def is_hotel_fully_booked(hotel_id: str) -> bool:
    r = requests.get(f"{BASE_URL}/api/hotels/{hotel_id}/fully-booked")
    assert r.status_code == 200
    return r.text == "true"


def get_user_status(user_id: str) -> str | None:
    r = requests.get(f"{BASE_URL}/api/users/{user_id}/status")
    match r.status_code:
        case 200:
            return r.text
        case 404:
            return None
        case _:
            raise AssertionError


class Promo(BaseModel):
    code: str
    discount: float
    vip_only: bool
    expired: bool
    valid_until: date
    description: str

    model_config = ConfigDict(
        alias_generator=alias_generators.to_camel,
        populate_by_name=True,
    )


def validate_promo(promo_code: str, user_id: str) -> Promo | None:
    r = requests.post(
        f"{BASE_URL}/api/promos/validate",
        data={"code": promo_code, "userId": user_id},
    )
    match r.status_code:
        case 200:
            return Promo.model_validate_json(r.text)
        case 400:
            return None
        case _:
            raise AssertionError
