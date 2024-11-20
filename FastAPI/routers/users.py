from fastapi import APIRouter, Path, File, UploadFile, status as st
from starlette.requests import Request

from main import app
from services import user_service as us
from schemas import CreateUserRequest, UserResponse, PrivateUserResponse, UpdateUserRequest, UpdateUserPasswordRequest, ImageResponse
from dependencies import user_dependency, db_dependency


router = APIRouter(prefix="/user", tags=["User"])


@router.post("/", response_model=UserResponse, status_code=st.HTTP_201_CREATED)
# Using stricter rate limiting to prevent spam user creation:
# Unsuccessful requests count towards the rate limit, so limits are still high:
@app.state.limiter.limit("10/minute, 100/hour, 300/day")
async def create_user(db: db_dependency, user_data: CreateUserRequest, request: Request):
    return us.create_user(db, user_data)


@router.get("/{user_id}", response_model=UserResponse, status_code=st.HTTP_200_OK)
@app.state.limiter.limit("10/minute")
async def read_user(db: db_dependency, request: Request, user_id: int = Path(ge=0)):
    return us.get_user(db, user_id)


@router.get("/", response_model=PrivateUserResponse, status_code=st.HTTP_200_OK)
@app.state.limiter.limit("100/minute")
async def read_current_user(user: user_dependency, request: Request):
    return user


@router.put("/", status_code=st.HTTP_204_NO_CONTENT)
@app.state.limiter.limit("10/minute")
async def update_user(db: db_dependency, user: user_dependency, user_data: UpdateUserRequest, request: Request):
    us.update_user(db, user, user_data)


@router.put("/password", status_code=st.HTTP_204_NO_CONTENT)
@app.state.limiter.limit("5/minute, 30/day")
async def update_user_password(db: db_dependency, user: user_dependency, password_data: UpdateUserPasswordRequest, request: Request):
    us.update_user_password(db, user, password_data)


@router.post("/profile", response_model=ImageResponse, status_code=st.HTTP_200_OK)
@app.state.limiter.limit("5/minute")
async def create_profile_image(db: db_dependency, user: user_dependency, request: Request, image: UploadFile = File(...)):
    return await us.create_profile_image(db, user, image)


@router.get("/{user_id}/profile", response_model=ImageResponse, status_code=st.HTTP_200_OK)
@app.state.limiter.limit("200/minute")
async def read_profile_image(db: db_dependency, request: Request, user_id: int = Path(ge=0)):
    return us.read_profile_image(db, user_id)


@router.delete("/profile", status_code=st.HTTP_204_NO_CONTENT)
@app.state.limiter.limit("5/minute")
async def delete_profile_image(db: db_dependency, user: user_dependency, request: Request):
    us.delete_profile_image(db, user)
    