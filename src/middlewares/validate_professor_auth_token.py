import os
import dotenv
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from repositories.professor_repository import ProfessorRepository

dotenv.load_dotenv()
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-default-secret-key")

def validate_professor_auth_token(request: Request):
    token = request.cookies.get("access_token")
    print(f"Validando token de professor: {token}")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token não encontrado"
        )
    
    try:
        # Remove o prefixo "Bearer " se existir
        if token.startswith("Bearer "):
            token = token[7:]
        
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=["HS256"])
        print(f"DEBUG: Payload do token: {payload}")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Token expirado")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Token inválido")

    # Verificar se o token é de um professor
    user_type = payload.get("type")
    if user_type != "professor":
        print(f"DEBUG: Tipo de usuário inválido: {user_type} (esperado: professor)")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Acesso negado: token não é de professor")

    professor_id = payload.get("sub")
    print(f"DEBUG: Professor ID extraído do token: {professor_id}")
    if not professor_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Credenciais inválidas")

    try:
        print(f"DEBUG: Tentando buscar professor com ID: {professor_id}")
        professor = ProfessorRepository().find_by_id(professor_id)
        print(f"DEBUG: Professor encontrado: {professor.name}")
    except ValueError as e:
        print(f"DEBUG: Erro ao buscar professor: {str(e)}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Professor não encontrado")
    except Exception as e:
        print(f"DEBUG: Erro inesperado ao buscar professor: {str(e)}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Erro interno na autenticação")

    return professor
