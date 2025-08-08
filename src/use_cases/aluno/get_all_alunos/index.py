from typing import List
from fastapi import APIRouter, Depends, HTTPException
from entities.aluno import Aluno
from repositories.aluno_repository import AlunoRepository
from use_cases.aluno.get_all_alunos.get_all_alunos_use_cases import GetAllAlunosUseCases
from middlewares.validate_admin_auth_token import validate_admin_auth_token

router = APIRouter()

repo = AlunoRepository()
get_all_alunos_uc = GetAllAlunosUseCases(repo)

@router.get(
    "/alunos",
    response_model=List[Aluno], dependencies=[Depends(validate_admin_auth_token)]
)
async def get_all_alunos():
    try:
        return get_all_alunos_uc.execute()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))