from fastapi import APIRouter, HTTPException, Request
from repositories.aluno_repository import AlunoRepository
from use_cases.aluno.login.login_aluno_use_case import LoginAlunoUseCase
from use_cases.aluno.login.login_aluno_dto import LoginAlunoDTO
from fastapi import Request, Response

router = APIRouter()

aluno_repository = AlunoRepository()
login_aluno_use_case = LoginAlunoUseCase(aluno_repository=aluno_repository)

@router.post("/alunos/login")
async def login_aluno(data: LoginAlunoDTO, request: Request, response: Response):
    try:
        result = login_aluno_use_case.execute(data, request, response)
        return {
            "aluno": {
                "id": str(result["aluno"].id),
                "name": result["aluno"].name,
                "email": result["aluno"].email
            }
        }
    except ValueError as e:
        raise HTTPException(
            status_code=401,
            detail=str(e)
        )
