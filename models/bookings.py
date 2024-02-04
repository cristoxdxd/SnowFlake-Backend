from pydantic import BaseModel
from datetime import date
from typing import List

class Bookings(BaseModel):
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
    availability: List[str]
    reviews: List[str]

    @classmethod
    def parse_availability(cls, value):
        return [date.fromisoformat(date_str) for date_str in value]
