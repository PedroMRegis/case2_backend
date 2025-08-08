from entities.aluno import Aluno
from repositories.aluno_repository import AlunoRepository
from use_cases.aluno.update_aluno.update_aluno_dto import UpdateAlunoDTO

class UpdateAlunoUseCase:
    def __init__(self, aluno_repository: AlunoRepository):
        self.aluno_repository = aluno_repository

    def execute(self, aluno_id: str, update_data: UpdateAlunoDTO) -> Aluno:
        """
        Atualiza os dados de um aluno pelo ID.
        Apenas admins podem executar esta ação.
        """
        try:
            # Verifica se o aluno existe
            aluno = self.aluno_repository.find_by_id(aluno_id)
            
            # Prepara os dados para atualização (apenas campos não nulos)
            update_dict = {}
            if update_data.name is not None:
                update_dict["name"] = update_data.name
            if update_data.email is not None:
                # Verifica se o email não está sendo usado por outro aluno
                try:
                    existing_aluno = self.aluno_repository.find_by_email(update_data.email)
                    if existing_aluno.id != aluno_id:
                        raise ValueError(f"Email '{update_data.email}' já está sendo usado por outro aluno")
                except ValueError as e:
                    if "não encontrado" not in str(e):
                        raise e  # Re-raise se for erro de email já existente
                update_dict["email"] = update_data.email
            if update_data.password is not None:
                update_dict["password"] = update_data.password
            if update_data.plano is not None:
                update_dict["plano"] = update_data.plano
            
            if not update_dict:
                raise ValueError("Nenhum campo válido para atualização foi fornecido")
            
            # Atualiza o aluno
            updated_aluno = self.aluno_repository.update_by_id(aluno_id, update_dict)
            return updated_aluno
            
        except ValueError as e:
            raise ValueError(str(e))
        except Exception as e:
            raise ValueError(f"Erro ao atualizar aluno: {str(e)}")
