import re
from pydantic import BaseModel, validator
from datetime import date

class Availability(BaseModel):
    booking_id: str
    start_date: date
    end_date: date
    user: str

    @validator('user')
    def validate_email(cls, email):
        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
            raise ValueError('Invalid email format')
        return email