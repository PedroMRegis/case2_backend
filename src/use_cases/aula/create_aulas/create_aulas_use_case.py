from repositories.aula_repository import AulaRepository
from repositories.professor_repository import ProfessorRepository
from use_cases.aula.create_aulas.create_aulas_dto import CreateAulasDTO
from entities.aula import Aula

class CreateAulasUseCase:
    def __init__(self, aula_repository: AulaRepository, professor_repository: ProfessorRepository):
        self.aula_repository = aula_repository
        self.professor_repository = professor_repository

    def execute(self, data: CreateAulasDTO, user_id: str, user_type: str) -> Aula:
        try:
            # Definir professor_id e aluno_id baseado no tipo de usuário
            if user_type == 'aluno':
                # Aluno logado: usa professor_id obrigatório e user_id como aluno
                if not data.professor_id:
                    raise ValueError("Aluno deve especificar o ID do professor")
                professor_id = data.professor_id
                aluno_id = user_id
                
            elif user_type == 'professor':
                # Professor logado: usa user_id como professor e aluno_id obrigatório
                professor_id = user_id  # Pega automaticamente do token
                if not data.aluno_id:
                    raise ValueError("Professor deve especificar o ID do aluno")
                aluno_id = data.aluno_id
                    
            else:
                raise ValueError("Tipo de usuário inválido")

            # Verificar se o professor existe
            try:
                professor = self.professor_repository.find_by_id(professor_id)
            except ValueError:
                raise ValueError("Professor não encontrado")

            # Criar a aula
            aula = Aula(
                date=data.date,
                professor_id=professor_id,
                aluno_id=aluno_id,
                status='agendada'
            )

            created_aula = self.aula_repository.save(aula)
            return created_aula
            
        except ValueError as e:
            raise ValueError(str(e))
        except Exception as e:
            raise Exception(f"Erro interno: {str(e)}")
