from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Literal

class PutAulasDTO(BaseModel):
    date: Optional[datetime] = None
    professor_id: Optional[str] = None
    status: Optional[Literal['agendada', 'concluida', 'cancelada']] = None
