from fastapi import APIRouter, HTTPException, Depends
from repositories.professor_repository import ProfessorRepository
from use_cases.professor.delete_professor.delete_professor_use_case import DeleteProfessorUseCase
from middlewares.validate_admin_auth_token import validate_admin_auth_token

router = APIRouter()

professor_repository = ProfessorRepository()
delete_professor_use_case = DeleteProfessorUseCase(professor_repository=professor_repository)

@router.delete(
    "/professores/{professor_id}",
    dependencies=[Depends(validate_admin_auth_token)]
)
async def delete_professor(professor_id: str):
    """
    Deleta um professor pelo ID.
    Requer autenticação de administrador.
    """
    try:
        delete_professor_use_case.execute(professor_id)
        return {"message": f"Professor com ID '{professor_id}' deletado com sucesso"}
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
