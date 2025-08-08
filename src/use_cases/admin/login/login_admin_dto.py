from pydantic import BaseModel, EmailStr

class LoginAdminDTO(BaseModel):
    email: EmailStr
    password: str
