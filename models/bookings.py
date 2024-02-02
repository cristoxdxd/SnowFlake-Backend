from pydantic import BaseModel
from datetime import date
from typing import List

class Bookings(BaseModel):
    id: str
    name: str
    description: str
    price: float
    capacity: int
    image: str
    availability: List[str]

    @classmethod
    def parse_availability(cls, value):
        return [date.fromisoformat(date_str) for date_str in value]
