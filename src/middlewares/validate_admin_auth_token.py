import os
import dotenv
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from repositories.admin_repository import AdminRepository


dotenv.load_dotenv()

security = HTTPBearer()
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")

def validate_admin_auth_token(request: Request):
    token = request.cookies.get("access_token")
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
        print(f"DEBUG: Payload do token admin: {payload}")
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

    # Verificar se o token é de um admin
    user_type = payload.get("type")
    if user_type != "admin":
        print(f"DEBUG: Tipo de usuário inválido: {user_type} (esperado: admin)")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Acesso negado: token não é de admin")

    admin_id = payload.get("sub")
    if not admin_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas",
        )

    try:
        # Busca o admin pelo ID decodificado
        admin = AdminRepository().find_by_id(admin_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Admin não encontrado",
        )

    return admin
