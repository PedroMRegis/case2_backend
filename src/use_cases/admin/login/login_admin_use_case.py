import os
import bcrypt
import jwt
from datetime import datetime, timedelta
from fastapi import Request, Response
from repositories.admin_repository import AdminRepository
from use_cases.admin.login.login_admin_dto import LoginAdminDTO

class LoginAdminUseCase:
    def __init__(self, admin_repository: AdminRepository):
        self.admin_repository = admin_repository

    def execute(self, login_data: LoginAdminDTO, request: Request, response: Response) -> dict:
        try:
            print(f"[LOGIN ADMIN] Tentando login para email: {login_data.email}")
            
            # Buscar admin por email
            admin = self.admin_repository.find_by_email(login_data.email)
            print(f"[LOGIN ADMIN] Admin encontrado: {admin.name}")
            
            # Verificar senha
            if not bcrypt.checkpw(login_data.password.encode(), admin.password.encode()):
                raise ValueError("Senha incorreta")

            # Gerar token JWT
            expiration = datetime.utcnow() + timedelta(hours=24)
            token = jwt.encode(
                {
                    "sub": str(admin.id),
                    "type": "admin",
                    "exp": expiration
                },
                os.getenv("JWT_SECRET_KEY", "your-default-secret-key"),
                algorithm="HS256"
            )
            
            print(f"[LOGIN ADMIN] Token gerado: {token[:50]}...")
            
            # Configurar cookie
            response.set_cookie(
                key="access_token",
                value=f"Bearer {token}",
                httponly=True,
                samesite="None",
                secure=True,
                path="/",
                max_age=86400
            )
            
            print("[LOGIN ADMIN] Cookie configurado com sucesso")

            return {
                "access_token": token,
                "token_type": "bearer",
                "admin": {
                    "id": admin.id,
                    "name": admin.name,
                    "email": admin.email
                }
            }
            
        except ValueError as e:
            print(f"[LOGIN ADMIN] Erro: {str(e)}")
            raise ValueError(str(e))
