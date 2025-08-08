from pydantic import BaseModel, EmailStr
from typing import Literal, Optional

class Aluno(BaseModel):
    id: Optional[str] = None
    name: str
    email: EmailStr
    password: str
    plano: Literal['individual', 'grupo']
