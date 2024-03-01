from fastapi import APIRouter, status as st

from dependencies import db_dependency, auth_dependency
from schemas import TokenResponse
from services import auth_service as aus


router = APIRouter(prefix="/auth", tags=["User Authentication"])

@router.post("/token", response_model=TokenResponse, status_code=st.HTTP_200_OK)
async def login_and_generate_token(user_input: auth_dependency, db: db_dependency):
    return aus.login_and_generate_token(user_input, db)