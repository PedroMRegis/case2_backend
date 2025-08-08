from pydantic import BaseModel, EmailStr

class LoginProfessorDTO(BaseModel):
    email: EmailStr
    password: str
