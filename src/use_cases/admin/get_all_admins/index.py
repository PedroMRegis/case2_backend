from typing import List
from fastapi import APIRouter, Depends, HTTPException
from entities.admin import Admin
from repositories.admin_repository import AdminRepository
from .get_all_admins_use_case import GetAllAdminsUseCase

router = APIRouter()

admin_repository = AdminRepository()
get_all_admins_uc = GetAllAdminsUseCase(admin_repository)

@router.get(
    "/admins",
    response_model=List[Admin]
)
async def get_all_admins():
    try:
        return get_all_admins_uc.execute()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
