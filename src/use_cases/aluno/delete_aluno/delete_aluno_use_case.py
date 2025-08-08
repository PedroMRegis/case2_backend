from repositories.aluno_repository import AlunoRepository

class DeleteAlunoUseCase:
    def __init__(self, aluno_repository: AlunoRepository):
        self.aluno_repository = aluno_repository

    def execute(self, aluno_id: str) -> None:
        """
        Deleta um aluno pelo ID.
        Apenas admins podem executar esta ação.
        """
        try:
            # Verifica se o aluno existe antes de deletar
            aluno = self.aluno_repository.find_by_id(aluno_id)
            
            # Deleta o aluno
            self.aluno_repository.delete_by_id(aluno_id)
            
        except ValueError as e:
            raise ValueError(str(e))
        except Exception as e:
            raise ValueError(f"Erro ao deletar aluno: {str(e)}")
