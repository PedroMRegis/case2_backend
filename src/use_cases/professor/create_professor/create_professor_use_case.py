from repositories.professor_repository import ProfessorRepository
from use_cases.professor.create_professor.create_professor_dto import CreateProfessorDTO
from entities.professor import Professor

class CreateProfessorUseCase:
    def __init__(self, professor_repository: ProfessorRepository):
        self.professor_repository = professor_repository

    def execute(self, data: CreateProfessorDTO) -> Professor:
        try:
            # Verificar se o email já existe
            try:
                existing_professor = self.professor_repository.find_by_email(data.email)
                # Se chegou aqui, o email já existe
                raise ValueError("Email já está em uso")
            except ValueError as e:
                # Se a mensagem for sobre email já em uso, propagar
                if "Email já está em uso" in str(e):
                    raise
                # Se não encontrou, está tudo certo (continua)
                pass
            
            # Criar o professor (o hash da senha será feito no repositório)
            professor = Professor(
                name=data.name,
                email=data.email,
                password=data.password,  # Senha sem hash aqui
                idioma=data.idioma,
                trilha=data.trilha
            )
            
            # Salvar no repositório
            return self.professor_repository.save(professor)
            
        except ValueError as e:
            raise ValueError(str(e))
        except Exception as e:
            raise Exception(f"Erro interno: {str(e)}")
