from fastapi import APIRouter, Depends, HTTPException, Request
from repositories.aula_repository import AulaRepository
from repositories.professor_repository import ProfessorRepository
from use_cases.aula.create_aulas.create_aulas_use_case import CreateAulasUseCase
from use_cases.aula.create_aulas.create_aulas_dto import CreateAulasDTO
from middlewares.validate_aluno_auth_token import validate_aluno_auth_token
from middlewares.validate_professor_auth_token import validate_professor_auth_token
from entities.aula import Aula

router = APIRouter()

aula_repository = AulaRepository()
professor_repository = ProfessorRepository()
create_aulas_use_case = CreateAulasUseCase(aula_repository, professor_repository)

def get_authenticated_user(request: Request):
    """
    Tenta autenticar como aluno primeiro, depois como professor
    Retorna (user, user_type) onde user_type é 'aluno' ou 'professor'
    """
    try:
        aluno = validate_aluno_auth_token(request)
        return aluno, 'aluno'
    except:
        try:
            professor = validate_professor_auth_token(request)
            return professor, 'professor'
        except:
            raise HTTPException(status_code=401, detail="Token de autenticação inválido")

@router.post(
    "/aulas",
    response_model=Aula
)
async def create_aula(data: CreateAulasDTO, request: Request):
    try:
        user, user_type = get_authenticated_user(request)
        return create_aulas_use_case.execute(data, str(user.id), user_type)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
