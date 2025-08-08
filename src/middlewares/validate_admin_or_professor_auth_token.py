import os
import dotenv
from fastapi import HTTPException, status, Request
import jwt
from repositories.admin_repository import AdminRepository
from repositories.professor_repository import ProfessorRepository

dotenv.load_dotenv()

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")

def validate_admin_or_professor_auth_token(request: Request):
    """
    Valida se o usuário é um admin ou professor autenticado.
    Retorna o tipo de usuário e seus dados.
    """
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token não encontrado"
        )
    
    # Remove o prefixo "Bearer " se existir
    if token.startswith("Bearer "):
        token = token[7:]
    
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=["HS256"])
        user_id = payload.get("sub")
        user_type = payload.get("type")
        
        if not user_id or not user_type:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido"
            )
        
        if user_type == "admin":
            admin_repository = AdminRepository()
            admin = admin_repository.find_by_id(user_id)
            return {"type": "admin", "user": admin}
        
        elif user_type == "professor":
            professor_repository = ProfessorRepository()
            professor = professor_repository.find_by_id(user_id)
            return {"type": "professor", "user": professor}
        
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Acesso negado. Apenas admins e professores podem acessar este recurso."
            )
            
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expirado"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido"
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
