from fastapi import APIRouter, status as st

from services import user_service as us
from schemas import CreateUserRequest, UserResponse
from dependencies import db_dependency

router = APIRouter(prefix="/user", tags=["User"])


@router.post("/", response_model=UserResponse, status_code=st.HTTP_201_CREATED)
async def create_user(request: CreateUserRequest, db: db_dependency):
    return us.create_user(request, db)
