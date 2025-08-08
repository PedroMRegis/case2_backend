from fastapi import APIRouter, HTTPException, Request, Response
from repositories.professor_repository import ProfessorRepository
from use_cases.professor.login.login_professor_use_case import LoginProfessorUseCase
from use_cases.professor.login.login_professor_dto import LoginProfessorDTO

router = APIRouter()

professor_repository = ProfessorRepository()
login_professor_use_case = LoginProfessorUseCase(professor_repository=professor_repository)

@router.post("/professores/login")
def login_professor(data: LoginProfessorDTO, request: Request, response: Response):
    try:
        result = login_professor_use_case.execute(data, request, response)
        # Retorna os dados do professor
        return {
            "professor": result["professor"]
        }
    except ValueError as e:
        raise HTTPException(
            status_code=401,
            detail=str(e)
        )
