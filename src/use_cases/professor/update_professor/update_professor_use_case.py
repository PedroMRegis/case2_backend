from entities.professor import Professor
from repositories.professor_repository import ProfessorRepository
from use_cases.professor.update_professor.update_professor_dto import UpdateProfessorDTO

class UpdateProfessorUseCase:
    def __init__(self, professor_repository: ProfessorRepository):
        self.professor_repository = professor_repository

    def execute(self, professor_id: str, update_data: UpdateProfessorDTO) -> Professor:
        """
        Atualiza os dados de um professor pelo ID.
        Apenas admins podem executar esta ação.
        """
        try:
            # Verifica se o professor existe
            professor = self.professor_repository.find_by_id(professor_id)
            
            # Prepara os dados para atualização (apenas campos não nulos)
            update_dict = {}
            if update_data.name is not None:
                update_dict["name"] = update_data.name
            if update_data.email is not None:
                # Verifica se o email não está sendo usado por outro professor
                try:
                    existing_professor = self.professor_repository.find_by_email(update_data.email)
                    if existing_professor.id != professor_id:
                        raise ValueError(f"Email '{update_data.email}' já está sendo usado por outro professor")
                except ValueError as e:
                    if "não encontrado" not in str(e):
                        raise e  # Re-raise se for erro de email já existente
                update_dict["email"] = update_data.email
            if update_data.password is not None:
                update_dict["password"] = update_data.password
            if update_data.idioma is not None:
                update_dict["idioma"] = update_data.idioma
            if update_data.trilha is not None:
                update_dict["trilha"] = update_data.trilha
            
            if not update_dict:
                raise ValueError("Nenhum campo válido para atualização foi fornecido")
            
            # Atualiza o professor
            updated_professor = self.professor_repository.update_by_id(professor_id, update_dict)
            return updated_professor
            
        except ValueError as e:
            raise ValueError(str(e))
        except Exception as e:
            raise ValueError(f"Erro ao atualizar professor: {str(e)}")
