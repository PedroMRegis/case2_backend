from fastapi import APIRouter, HTTPException, Depends
from repositories.professor_repository import ProfessorRepository
from use_cases.professor.update_professor.update_professor_use_case import UpdateProfessorUseCase
from use_cases.professor.update_professor.update_professor_dto import UpdateProfessorDTO
from middlewares.validate_admin_auth_token import validate_admin_auth_token
from entities.professor import Professor

router = APIRouter()

professor_repository = ProfessorRepository()
update_professor_use_case = UpdateProfessorUseCase(professor_repository=professor_repository)

@router.put(
    "/professores/{professor_id}",
    response_model=Professor,
    dependencies=[Depends(validate_admin_auth_token)]
)
async def update_professor(professor_id: str, update_data: UpdateProfessorDTO):
    """
    Atualiza os dados de um professor pelo ID.
    Requer autenticação de administrador.
    
    Campos opcionais:
    - name: Nome do professor
    - email: Email do professor (deve ser único)
    - password: Nova senha (será criptografada)
    - idioma: Idioma do professor ("ingles" ou "espanhol")
    - trilha: Trilha do professor ("financeiro" ou "corporativo")
    """
    try:
        updated_professor = update_professor_use_case.execute(professor_id, update_data)
        return updated_professor
    except ValueError as e:
        if "não encontrado" in str(e) or "ID inválido" in str(e):
            raise HTTPException(
                status_code=404,
                detail=str(e)
            )
        else:
            raise HTTPException(
                status_code=400,
                detail=str(e)
            )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro interno: {str(e)}"
        )
