from fastapi import APIRouter, Depends, HTTPException
from repositories.admin_repository import AdminRepository
from use_cases.admin.create_admin.create_admin_use_cases import CreateAdminUseCases
from use_cases.admin.create_admin.create_admin_dto import CreateAdminDTO
from entities.admin import Admin

router = APIRouter()

admin_repository = AdminRepository()
create_admin_use_case = CreateAdminUseCases(admin_repository=admin_repository)

@router.post(
    "/admins",
    response_model=list[Admin]
)
def create_admin(data: CreateAdminDTO):
    try:
        admin = create_admin_use_case.execute(data)
        return [admin]
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro interno: {str(e)}"
        )
