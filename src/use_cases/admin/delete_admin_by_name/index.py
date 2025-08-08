from fastapi import APIRouter, Depends, HTTPException
from repositories.admin_repository import AdminRepository
from .delete_admin_by_name_use_case import DeleteAdminByNameUseCase
from middlewares.validate_admin_auth_token import validate_admin_auth_token

router = APIRouter()

adminrepository = AdminRepository()
delete_by_name_uc = DeleteAdminByNameUseCase(adminrepository)

@router.delete(
    "/admins/{name}",
    dependencies=[Depends(validate_admin_auth_token)]
)
async def delete_admin_by_name(name: str):
    """
    Deleta um administrador pelo nome.
    """
    try:
        delete_by_name_uc.execute(name)
        return {"message": f"Admin '{name}' deletado com sucesso"}
    except ValueError as e:
        # nome não encontrado
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        # outros erros
        raise HTTPException(status_code=500, detail=str(e))
