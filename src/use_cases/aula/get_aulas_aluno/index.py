from fastapi import APIRouter, Depends, HTTPException, Request
from repositories.aula_repository import AulaRepository
from repositories.professor_repository import ProfessorRepository
from repositories.aluno_repository import AlunoRepository
from use_cases.aula.get_aulas_aluno.get_aulas_aluno_use_case import GetAulasAlunoUseCase
from middlewares.validate_aluno_auth_token import validate_aluno_auth_token

router = APIRouter()

aula_repository = AulaRepository()
professor_repository = ProfessorRepository()
aluno_repository = AlunoRepository()
get_aulas_aluno_use_case = GetAulasAlunoUseCase(aula_repository, professor_repository, aluno_repository)

@router.get("/aluno/aulas")
async def get_aulas_aluno(request: Request):
    try:
        # Autenticar apenas como aluno
        aluno = validate_aluno_auth_token(request)
        print(f"DEBUG: Aluno autenticado - ID: {aluno.id}, Nome: {aluno.name}")
        
        # Buscar aulas do aluno
        aulas = get_aulas_aluno_use_case.execute(str(aluno.id))
        
        return {
            "aulas": aulas,
            "total": len(aulas),
            "aluno": {
                "id": str(aluno.id),
                "name": aluno.name,
                "email": aluno.email
            }
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print(f"DEBUG: Erro no endpoint aluno/aulas: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
