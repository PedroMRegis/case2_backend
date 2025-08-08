import os
import dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from repositories.aluno_repository import AlunoRepository
from fastapi import Request


dotenv.load_dotenv()

security = HTTPBearer()
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-default-secret-key")

def validate_aluno_auth_token(request: Request):
    token = request.cookies.get("access_token")
    print(f"Validando token: {token}")
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
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expirado",
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido",
        )

    aluno_id = payload.get("sub")
    if not aluno_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas",
        )

    try:
        # Busca o aluno pelo ID decodificado
        aluno = AlunoRepository().find_by_id(aluno_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Aluno não encontrado",
        )

    return aluno
