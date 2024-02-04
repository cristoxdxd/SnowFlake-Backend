from pydantic import BaseModel
from datetime import datetime
from typing import List

class Activities(BaseModel):
    id_act: str
    name: str
    description: str
    price: float
    outside_activity: bool
    duration: int
    images: List[str]
    availability: List[datetime]  # Cambiado a datetime para incluir fecha y hora
    reviews: List[str]

    @classmethod
    def parse_availability(cls, value):
        return [datetime.fromisoformat(date_str) for date_str in value]
