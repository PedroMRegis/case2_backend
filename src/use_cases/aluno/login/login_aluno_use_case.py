import os
import bcrypt
import jwt
from datetime import datetime, timedelta
from repositories.aluno_repository import AlunoRepository
from use_cases.aluno.login.login_aluno_dto import LoginAlunoDTO
from fastapi import Request, Response

class LoginAlunoUseCase:
    def __init__(self, aluno_repository: AlunoRepository):
        self.aluno_repository = aluno_repository

    def execute(self, login_data: LoginAlunoDTO, request: Request, response: Response) -> dict:
        try:
            # Buscar aluno por email
            print(f"Buscando aluno com email: {login_data.email}")
            aluno = self.aluno_repository.find_by_email(login_data.email)
            
            # Verificar senha
            if not bcrypt.checkpw(login_data.password.encode(), aluno.password.encode()):
                raise ValueError("Senha incorreta")

            # Gerar token JWT
            expiration = datetime.utcnow() + timedelta(hours=24)
            token = jwt.encode(
                {
                    "sub": str(aluno.id),
                    "type": "aluno",
                    "exp": expiration
                },
                os.getenv("JWT_SECRET_KEY", "your-default-secret-key"),
                algorithm="HS256"
            )
            
            response.set_cookie(
                key="access_token",
                value=f"Bearer {token}",
                httponly=True,
                samesite="None",
                secure=True,
                path="/"
            )

            return {
                "access_token": token,
                "token_type": "bearer",
                "aluno": aluno
            }
            
        except ValueError as e:
            raise ValueError(str(e))
