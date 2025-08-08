from repositories.aula_repository import AulaRepository
from repositories.professor_repository import ProfessorRepository
from use_cases.aula.put_aula.put_aulas_dto import PutAulasDTO
from entities.aula import Aula

class PutAulaUseCase:
    def __init__(self, aula_repository: AulaRepository, professor_repository: ProfessorRepository):
        self.aula_repository = aula_repository
        self.professor_repository = professor_repository

    def execute(self, aula_id: str, data: PutAulasDTO, user_id: str, user_type: str) -> Aula:
        try:
            # Buscar a aula por ID
            aula = self.aula_repository.find_by_id(aula_id)
            if not aula:
                raise ValueError("Aula não encontrada")

            # Verificar permissões baseado no tipo de usuário
            if user_type == 'aluno':
                # Aluno só pode editar suas próprias aulas
                if aula.aluno_id != user_id:
                    raise ValueError("Você não tem permissão para atualizar esta aula")
            elif user_type == 'professor':
                # Professor pode editar aulas onde ele é o professor
                if aula.professor_id != user_id:
                    raise ValueError("Você não tem permissão para atualizar esta aula")
            else:
                raise ValueError("Tipo de usuário inválido")

            # Verificar se a aula ainda pode ser atualizada
            if aula.status == 'concluida' and data.status != 'concluida':
                raise ValueError("Não é possível alterar uma aula já concluída")

            # Validar professor se fornecido
            if data.professor_id:
                professor = self.professor_repository.find_by_id(data.professor_id)
                if not professor:
                    raise ValueError("Professor não encontrado")

            # Preparar dados para atualização
            update_data = {}
            
            if data.date is not None:
                update_data['date'] = data.date
            if data.professor_id is not None:
                update_data['professor_id'] = data.professor_id
            if data.status is not None:
                update_data['status'] = data.status

            # Atualizar no repositório
            return self.aula_repository.update(aula_id, update_data)
            
        except ValueError as e:
            raise ValueError(str(e))
        except Exception as e:
            raise Exception(f"Erro interno: {str(e)}")
