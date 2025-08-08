from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class CreateAulasDTO(BaseModel):
    date: datetime
    professor_id: Optional[str] = None  # ID do professor (opcional para quando professor cria)
    aluno_id: Optional[str] = None  # ID do aluno (opcional para quando aluno cria)
