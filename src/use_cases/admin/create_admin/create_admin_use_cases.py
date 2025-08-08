import bcrypt
from entities.admin import Admin
from repositories.admin_repository import AdminRepository
from use_cases.admin.create_admin.create_admin_dto import CreateAdminDTO

class CreateAdminUseCases:
    def __init__(self, admin_repository: AdminRepository):
        self.admin_repository = admin_repository

    def execute(self, admin_data: CreateAdminDTO) -> Admin:
        # Verificar se já existe admin com esse email
        try:
            existing_admin = self.admin_repository.find_by_email(admin_data.email)
            raise ValueError(f"Admin com email '{admin_data.email}' já existe")
        except ValueError as e:
            if "não encontrado" not in str(e):
                raise e  # Re-raise se for erro de email já existente
        
        # Criar novo admin (o repository vai gerar o ID)
        admin = Admin(
            id="temp_id",  # Temporário, será substituído pelo repository
            name=admin_data.name,
            email=admin_data.email,
            password=admin_data.password
        )
        
        return self.admin_repository.save(admin)
