import dotenv
from pydantic import BaseModel


dotenv.load_dotenv()

class Admin(BaseModel):
    id: str
    name: str
    email: str
    password: str