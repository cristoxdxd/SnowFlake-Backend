from pydantic import BaseModel

class Email(BaseModel):
    email: str
    asunto: str
    contenido:str