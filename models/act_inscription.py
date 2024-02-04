from pydantic import BaseModel
from datetime import datetime
from typing import List

class Act_Inscription(BaseModel):
    id_ins: str
    usr_name: str
    price: float
