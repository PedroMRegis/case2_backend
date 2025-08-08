from pydantic import BaseModel, EmailStr

class LoginAlunoDTO(BaseModel):
    email: EmailStr
    password: str
