from fastapi import APIRouter, HTTPException, Request
from repositories.professor_repository import ProfessorRepository
from use_cases.professor.get_all_professores.get_all_professores_use_case import GetAllProfessoresUseCase
from middlewares.validate_aluno_auth_token import validate_aluno_auth_token
from middlewares.validate_admin_auth_token import validate_admin_auth_token

router = APIRouter()

professor_repository = ProfessorRepository()
get_all_professores_use_case = GetAllProfessoresUseCase(professor_repository)

def get_authenticated_user(request: Request):
    """
    Tenta autenticar como aluno ou admin
    Retorna (user, user_type) onde user_type é 'aluno' ou 'admin'
    """
    try:
        aluno = validate_aluno_auth_token(request)
        return aluno, 'aluno'
    except:
        try:
            admin = validate_admin_auth_token(request)
            return admin, 'admin'
        except:
            raise HTTPException(status_code=401, detail="Token de autenticação inválido")

@router.get("/professores")
async def get_all_professores(request: Request):
    try:
        user, user_type = get_authenticated_user(request)
        professores = get_all_professores_use_case.execute(str(user.id), user_type)
        
        return {
            "professores": professores
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
