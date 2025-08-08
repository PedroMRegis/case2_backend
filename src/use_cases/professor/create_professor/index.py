from fastapi import APIRouter, HTTPException
from repositories.professor_repository import ProfessorRepository
from use_cases.professor.create_professor.create_professor_use_case import CreateProfessorUseCase
from use_cases.professor.create_professor.create_professor_dto import CreateProfessorDTO
from entities.professor import Professor

router = APIRouter()

professor_repository = ProfessorRepository()
create_professor_use_case = CreateProfessorUseCase(professor_repository)

@router.post("/professores", response_model=Professor)
async def create_professor(data: CreateProfessorDTO):
    try:
        return create_professor_use_case.execute(data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
