from fastapi import APIRouter, Depends, HTTPException
from repositories.aluno_repository import AlunoRepository
from use_cases.aluno.create_alunos.create_alunos_use_cases import CreateAlunoUseCases
from use_cases.aluno.create_alunos.create_alunos_dto import CreateAlunoDTO
from entities.aluno import Aluno

router = APIRouter()

aluno_repository = AlunoRepository()
create_aluno_use_case = CreateAlunoUseCases(aluno_repository=aluno_repository)

@router.post(
    "/alunos",
    response_model=Aluno,
    status_code=201
)
def create_aluno(data: CreateAlunoDTO):
    try:
        aluno = create_aluno_use_case.execute(data)
        return aluno
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
