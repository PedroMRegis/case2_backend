from repositories.admin_repository import AdminRepository

class DeleteAdminByNameUseCase:
    def __init__(self, admin_repository: AdminRepository):
        self.admin_repository = admin_repository

    def execute(self, name: str) -> None:
        self.admin_repository.delete_by_name(name)