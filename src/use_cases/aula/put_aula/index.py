from fastapi import APIRouter, Depends, HTTPException, Request
from repositories.aula_repository import AulaRepository
from repositories.professor_repository import ProfessorRepository
from use_cases.aula.put_aula.put_aula_use_case import PutAulaUseCase
from use_cases.aula.put_aula.put_aulas_dto import PutAulasDTO
from middlewares.validate_aluno_auth_token import validate_aluno_auth_token
from middlewares.validate_professor_auth_token import validate_professor_auth_token
from entities.aula import Aula

router = APIRouter()

aula_repository = AulaRepository()
professor_repository = ProfessorRepository()
put_aula_use_case = PutAulaUseCase(aula_repository, professor_repository)

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

@router.put("/aulas/{aula_id}", response_model=Aula)
async def update_aula(aula_id: str, data: PutAulasDTO, request: Request):
    try:
        user, user_type = get_authenticated_user(request)
        return put_aula_use_case.execute(aula_id, data, str(user.id), user_type)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
