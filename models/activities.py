from pydantic import BaseModel
from datetime import datetime
from typing import List

class Activities(BaseModel):
    id_act: str
    name: str
    description: str
    price: float
    duration: int
    image: str