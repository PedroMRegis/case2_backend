from pydantic import BaseModel, EmailStr
from typing import Literal

class CreateAlunoDTO(BaseModel):
    name: str
    email: EmailStr
    password: str
    plano: Literal['individual', 'grupo']
