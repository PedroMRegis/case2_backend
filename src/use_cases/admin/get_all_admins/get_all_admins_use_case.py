from typing import List
from entities.admin import Admin
from repositories.admin_repository import AdminRepository

class GetAllAdminsUseCase:
    def __init__(self, admin_repository: AdminRepository):
        self.admin_repository = admin_repository

    def execute(self) -> List[Admin]:
        return self.admin_repository.find_all()