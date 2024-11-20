from fastapi import APIRouter, status as st
from starlette.requests import Request

from main import app
from dependencies import db_dependency, auth_dependency
from schemas import TokenResponse
from services import auth_service as aus


router = APIRouter(prefix="/auth", tags=["User Authentication"])


# TODO: Include all possible status codes in decorator.
@router.post("/token", response_model=TokenResponse, status_code=st.HTTP_200_OK)
# Using stricter rate limiting to prevent abuse of the login endpoint:
@app.state.limiter.limit("3/second, 120/minute")
# SlowAPI uses an argument with identifier "request" or "websocket" to identify the client:
# We need this in all endpoints since we have a default rate limit set:
async def login_and_generate_token(db: db_dependency, auth_form: auth_dependency, request: Request):
    return aus.login_and_generate_token(db, auth_form)