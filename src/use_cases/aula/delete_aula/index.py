from fastapi import APIRouter, Depends, HTTPException, Request
from repositories.aula_repository import AulaRepository
from use_cases.aula.delete_aula.delete_aula_use_cases import DeleteAulaUseCase
from middlewares.validate_aluno_auth_token import validate_aluno_auth_token
from middlewares.validate_professor_auth_token import validate_professor_auth_token

router = APIRouter()

aula_repository = AulaRepository()
delete_aula_use_case = DeleteAulaUseCase(aula_repository)

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

@router.delete("/aulas/{aula_id}")
async def delete_aula(aula_id: str, request: Request):
    try:
        user, user_type = get_authenticated_user(request)
        result = delete_aula_use_case.execute(aula_id, str(user.id), user_type)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
