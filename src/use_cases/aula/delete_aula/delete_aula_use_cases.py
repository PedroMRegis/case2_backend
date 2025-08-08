from repositories.aula_repository import AulaRepository

class DeleteAulaUseCase:
    def __init__(self, aula_repository: AulaRepository):
        self.aula_repository = aula_repository

    def execute(self, aula_id: str, user_id: str, user_type: str) -> dict:
        try:
            # Validar formato do ID
            if not aula_id or len(aula_id) != 24:
                raise ValueError("ID da aula inválido")

            # Buscar a aula por ID
            try:
                aula = self.aula_repository.find_by_id(aula_id)
            except ValueError:
                raise ValueError("Aula não encontrada")

            # Verificar permissões baseado no tipo de usuário
            if user_type == 'aluno':
                # Aluno só pode deletar suas próprias aulas
                if aula.aluno_id != user_id:
                    raise ValueError("Você não tem permissão para deletar esta aula (não é seu agendamento)")
            elif user_type == 'professor':
                # Professor pode deletar aulas onde ele é o professor
                if aula.professor_id != user_id:
                    raise ValueError("Você não tem permissão para deletar esta aula (não é sua aula)")
            else:
                raise ValueError("Tipo de usuário inválido")

            # Deletar a aula (removido a verificação de status - pode deletar qualquer status)
            self.aula_repository.delete(aula_id)
            
            return {"message": f"Aula deletada com sucesso (status: {aula.status})"}
            
        except ValueError as e:
            raise ValueError(str(e))
        except Exception as e:
            raise Exception(f"Erro interno ao deletar aula: {str(e)}")
