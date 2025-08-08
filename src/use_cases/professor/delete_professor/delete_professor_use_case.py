from repositories.professor_repository import ProfessorRepository

class DeleteProfessorUseCase:
    def __init__(self, professor_repository: ProfessorRepository):
        self.professor_repository = professor_repository

    def execute(self, professor_id: str) -> None:
        """
        Deleta um professor pelo ID.
        Apenas admins podem executar esta ação.
        """
        try:
            # Verifica se o professor existe antes de deletar
            professor = self.professor_repository.find_by_id(professor_id)
            
            # Deleta o professor
            self.professor_repository.delete_by_id(professor_id)
            
        except ValueError as e:
            raise ValueError(str(e))
        except Exception as e:
            raise ValueError(f"Erro ao deletar professor: {str(e)}")
