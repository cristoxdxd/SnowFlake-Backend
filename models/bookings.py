from pydantic import BaseModel
from datetime import date
from typing import List
from .user import User


class Bookings(BaseModel):
    id: int
    name: str
    summary: str
    description: str
    capacity: int
    price: float
    room_type: str
    bed_type: str
    minimum_nights: int
    maximum_nights: int
    bedrooms: int
    beds: int
    bathrooms: int
    images: List[str]
    availability: List[User]  # Cambio a una lista de usuarios
    reviews: List[str]

    @classmethod
    def parse_availability(cls, value):
        return [User(email=user['email']) for user in value]
