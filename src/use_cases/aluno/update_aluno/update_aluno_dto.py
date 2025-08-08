from pydantic import BaseModel, EmailStr
from typing import Optional, Literal

class UpdateAlunoDTO(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    plano: Optional[Literal["individual", "grupo"]] = None
