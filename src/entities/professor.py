from pydantic import BaseModel, EmailStr
from typing import Literal, Optional

class Professor(BaseModel):
    id: Optional[str] = None
    name: str
    email: EmailStr
    password: str
    idioma: Literal['ingles', 'espanhol']
    trilha: Literal['financeiro', 'corporativo']
    

