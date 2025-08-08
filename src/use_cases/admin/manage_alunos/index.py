from typing import List
from fastapi import APIRouter, Depends, HTTPException
from repositories.aluno_repository import AlunoRepository
from entities.aluno import Aluno
from .get_all_alunos_admin_use_case import GetAllAlunosAdminUseCase
from middlewares.validate_admin_auth_token import validate_admin_auth_token

router = APIRouter(prefix="/admin", tags=["Admin"])

aluno_repository = AlunoRepository()
get_all_alunos_admin_uc = GetAllAlunosAdminUseCase(aluno_repository)

@router.get(
    "/alunos",
    response_model=List[Aluno],
    dependencies=[Depends(validate_admin_auth_token)]
)
async def get_all_alunos_admin():
    """
    Lista todos os alunos (endpoint administrativo).
    Requer autenticação de administrador.
    """
    try:
        return get_all_alunos_admin_uc.execute()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
