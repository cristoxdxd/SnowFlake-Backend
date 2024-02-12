from pydantic import BaseModel
from datetime import date

class Availability(BaseModel):
    booking_id: str
    start_date: str
    end_date: str
    user: str
    
    @classmethod
    def parse_availability(cls, availability):
        return cls(
            booking_id=availability["booking_id"],
            start_date=date.fromisoformat(availability["start_date"]),
            end_date=date.fromisoformat(availability["end_date"]),
            user=availability["user"]
        )
    
