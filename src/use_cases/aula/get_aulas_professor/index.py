from fastapi import APIRouter, Depends, HTTPException, Request
from repositories.aula_repository import AulaRepository
from repositories.professor_repository import ProfessorRepository
from repositories.aluno_repository import AlunoRepository
from use_cases.aula.get_aulas_professor.get_aulas_professor_use_case import GetAulasProfessorUseCase
from middlewares.validate_professor_auth_token import validate_professor_auth_token

router = APIRouter()

aula_repository = AulaRepository()
professor_repository = ProfessorRepository()
aluno_repository = AlunoRepository()
get_aulas_professor_use_case = GetAulasProfessorUseCase(aula_repository, professor_repository, aluno_repository)

@router.get("/professores/aulas")
async def get_aulas_professor(request: Request):
    try:
        # Autenticar apenas como professor
        professor = validate_professor_auth_token(request)
        print(f"DEBUG: Professor autenticado - ID: {professor.id}, Nome: {professor.name}")
        
        # Buscar aulas do professor
        aulas = get_aulas_professor_use_case.execute(str(professor.id))
        
        return {
            "aulas": aulas,
            "total": len(aulas),
            "professor": {
                "id": str(professor.id),
                "name": professor.name,
                "idioma": professor.idioma,
                "trilha": professor.trilha
            }
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print(f"DEBUG: Erro no endpoint professor/aulas: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
