import os
import bcrypt
import jwt
from datetime import datetime, timedelta
from repositories.professor_repository import ProfessorRepository
from use_cases.professor.login.login_professor_dto import LoginProfessorDTO
from fastapi import Request, Response

class LoginProfessorUseCase:
    def __init__(self, professor_repository: ProfessorRepository):
        self.professor_repository = professor_repository

    def execute(self, login_data: LoginProfessorDTO, request: Request, response: Response) -> dict:
        try:
            # Buscar professor por email
            print(f"DEBUG: Buscando professor com email: {login_data.email}")
            professor = self.professor_repository.find_by_email(login_data.email)
            
            # Verificar senha
            if not bcrypt.checkpw(login_data.password.encode(), professor.password.encode()):
                raise ValueError("Senha incorreta")

            # Gerar token JWT
            expiration = datetime.utcnow() + timedelta(hours=24)
            token = jwt.encode(
                {
                    "sub": str(professor.id),
                    "type": "professor",
                    "exp": expiration
                },
                os.getenv("JWT_SECRET_KEY", "your-default-secret-key"),
                algorithm="HS256"
            )
            
            print(f"DEBUG: Token gerado para professor: {token[:20]}...")
            
            # Configura o cookie com o token
            response.set_cookie(
                key="access_token",
                value=f"Bearer {token}",
                httponly=True,
                samesite="None",
                secure=True,
                path="/",
                max_age=86400
            )
            
            print("DEBUG: Cookie configurado no response")

            return {
                "access_token": token,
                "token_type": "bearer",
                "professor": {
                    "id": professor.id,
                    "name": professor.name,
                    "email": professor.email,
                    "idioma": professor.idioma,
                    "trilha": professor.trilha
                }
            }
            
        except ValueError as e:
            raise ValueError(str(e))
