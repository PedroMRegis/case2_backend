from fastapi import APIRouter, HTTPException, Depends
from repositories.admin_repository import AdminRepository
from use_cases.admin.delete_admin_by_id.delete_admin_by_id_use_case import DeleteAdminByIdUseCase
from middlewares.validate_admin_auth_token import validate_admin_auth_token

router = APIRouter()

admin_repository = AdminRepository()
delete_admin_by_id_use_case = DeleteAdminByIdUseCase(admin_repository=admin_repository)

@router.delete(
    "/admins/id/{admin_id}",
    dependencies=[Depends(validate_admin_auth_token)]
)
async def delete_admin_by_id(admin_id: str):
    """
    Deleta um administrador pelo ID.
    Requer autenticação de administrador.
    """
    try:
        delete_admin_by_id_use_case.execute(admin_id)
        return {"message": f"Admin com ID '{admin_id}' deletado com sucesso"}
    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro interno: {str(e)}"
        )
