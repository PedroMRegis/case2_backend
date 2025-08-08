from pydantic import BaseModel
from typing import Literal, Optional
from datetime import datetime 

class Aula(BaseModel):
    id: Optional[str] = None
    date: datetime
    professor_id: str
    aluno_id: str
    status: Literal['agendada', 'concluida', 'cancelada'] = 'agendada'

