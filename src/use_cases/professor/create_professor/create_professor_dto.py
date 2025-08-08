from pydantic import BaseModel, EmailStr
from typing import Literal

class CreateProfessorDTO(BaseModel):
    name: str
    email: EmailStr
    password: str
    idioma: Literal['ingles', 'espanhol']
    trilha: Literal['financeiro', 'corporativo']
