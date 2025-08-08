from repositories.admin_repository import AdminRepository

class DeleteAdminByIdUseCase:
    def __init__(self, admin_repository: AdminRepository):
        self.admin_repository = admin_repository

    def execute(self, admin_id: str) -> None:
        """
        Deleta um admin pelo ID.
        Apenas admins podem executar esta ação.
        """
        try:
            # Verifica se o admin existe antes de deletar
            admin = self.admin_repository.find_by_id(admin_id)
            
            # Deleta o admin
            self.admin_repository.delete_by_id(admin_id)
            
        except ValueError as e:
            raise ValueError(str(e))
        except Exception as e:
            raise ValueError(f"Erro ao deletar admin: {str(e)}")
