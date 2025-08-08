from typing import List
from entities.aluno import Aluno
from repositories.aluno_repository import AlunoRepository

class GetAllAlunosUseCases:
    def __init__(self, aluno_repository: AlunoRepository):
        self.aluno_repository = aluno_repository

    def execute(self) -> List[Aluno]:
        return self.aluno_repository.find_all()