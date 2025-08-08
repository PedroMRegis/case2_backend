from pydantic import BaseModel, EmailStr
from typing import Optional, Literal

class UpdateProfessorDTO(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    idioma: Optional[Literal["ingles", "espanhol"]] = None
    trilha: Optional[Literal["financeiro", "corporativo"]] = None
