from fastapi import APIRouter, HTTPException, Depends
from repositories.aluno_repository import AlunoRepository
from use_cases.aluno.delete_aluno.delete_aluno_use_case import DeleteAlunoUseCase
from middlewares.validate_admin_auth_token import validate_admin_auth_token

router = APIRouter()

aluno_repository = AlunoRepository()
delete_aluno_use_case = DeleteAlunoUseCase(aluno_repository=aluno_repository)

@router.delete(
    "/alunos/{aluno_id}",
    dependencies=[Depends(validate_admin_auth_token)]
)
async def delete_aluno(aluno_id: str):
    """
    Deleta um aluno pelo ID.
    Requer autenticação de administrador.
    """
    try:
        delete_aluno_use_case.execute(aluno_id)
        return {"message": f"Aluno com ID '{aluno_id}' deletado com sucesso"}
    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro interno: {str(e)}"
        )
