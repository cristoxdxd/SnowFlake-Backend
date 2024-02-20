from pydantic import BaseModel

class Activities(BaseModel):
    name: str
    description: str
    price: float
    duration: int
    image: str