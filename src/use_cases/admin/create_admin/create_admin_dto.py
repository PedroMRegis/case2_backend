from pydantic import BaseModel, EmailStr

class CreateAdminDTO(BaseModel):
    name: str
    email: EmailStr
    password: str

