from fastapi import APIRouter, HTTPException, Depends
from repositories.aluno_repository import AlunoRepository
from use_cases.aluno.update_aluno.update_aluno_use_case import UpdateAlunoUseCase
from use_cases.aluno.update_aluno.update_aluno_dto import UpdateAlunoDTO
from middlewares.validate_admin_auth_token import validate_admin_auth_token
from entities.aluno import Aluno

router = APIRouter()

aluno_repository = AlunoRepository()
update_aluno_use_case = UpdateAlunoUseCase(aluno_repository=aluno_repository)

@router.put(
    "/alunos/{aluno_id}",
    response_model=Aluno,
    dependencies=[Depends(validate_admin_auth_token)]
)
async def update_aluno(aluno_id: str, update_data: UpdateAlunoDTO):
    """
    Atualiza os dados de um aluno pelo ID.
    Requer autenticação de administrador.
    
    Campos opcionais:
    - name: Nome do aluno
    - email: Email do aluno (deve ser único)
    - password: Nova senha (será criptografada)
    - plano: Plano do aluno ("basico" ou "premium")
    """
    try:
        updated_aluno = update_aluno_use_case.execute(aluno_id, update_data)
        return updated_aluno
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
