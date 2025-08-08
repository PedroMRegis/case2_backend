from typing import List
from repositories.aluno_repository import AlunoRepository
from entities.aluno import Aluno

class GetAllAlunosAdminUseCase:
    def __init__(self, aluno_repository: AlunoRepository):
        self.aluno_repository = aluno_repository

    def execute(self) -> List[Aluno]:
        return self.aluno_repository.find_all()
