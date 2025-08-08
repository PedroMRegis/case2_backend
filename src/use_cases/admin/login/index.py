from fastapi import APIRouter, HTTPException, Request, Response
from repositories.admin_repository import AdminRepository
from use_cases.admin.login.login_admin_use_case import LoginAdminUseCase
from use_cases.admin.login.login_admin_dto import LoginAdminDTO

router = APIRouter()

admin_repository = AdminRepository()
login_admin_use_case = LoginAdminUseCase(admin_repository=admin_repository)

@router.post("/admins/login")
def login_admin(data: LoginAdminDTO, request: Request, response: Response):
    try:
        result = login_admin_use_case.execute(data, request, response)
        # Retorna os dados do admin
        return {
            "admin": result["admin"]
        }
    except ValueError as e:
        raise HTTPException(
            status_code=401,
            detail=str(e)
        )
