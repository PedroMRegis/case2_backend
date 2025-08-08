from fastapi import APIRouter, Depends, HTTPException, Request
from repositories.aula_repository import AulaRepository
from repositories.professor_repository import ProfessorRepository
from repositories.aluno_repository import AlunoRepository
from use_cases.aula.get_aulas_admin.get_aulas_admin_use_case import GetAulasAdminUseCase
from middlewares.validate_admin_auth_token import validate_admin_auth_token

router = APIRouter()

aula_repository = AulaRepository()
professor_repository = ProfessorRepository()
aluno_repository = AlunoRepository()
get_aulas_admin_use_case = GetAulasAdminUseCase(aula_repository, professor_repository, aluno_repository)

@router.get("/admin/aulas")
async def get_aulas_admin(request: Request):
    try:
        # Autenticar apenas como admin
        admin = validate_admin_auth_token(request)
        print(f"DEBUG: Admin autenticado - ID: {admin.id}, Nome: {admin.name}")
        
        # Buscar todas as aulas
        aulas = get_aulas_admin_use_case.execute()
        
        return {
            "aulas": aulas,
            "total": len(aulas),
            "admin": {
                "id": str(admin.id),
                "name": admin.name
            }
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print(f"DEBUG: Erro no endpoint admin/aulas: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
