from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status as st

from dependencies import db_dependency
from schemas import CreateUserRequest, UserResponse
from models import User
from security import bcrypt_context


def create_user(request: CreateUserRequest, db: db_dependency) -> UserResponse:
    # TODO: incorporate CAPTCHA for user creation

    # Hashing the password:
    password_hash = bcrypt_context.hash(request.password)

    # Creating a new user instance with the hashed password instead of plaintext:
    new_user = User(**request.dict(exclude={"password"}), password=password_hash)

    try:
        db.add(new_user)
        db.commit()

        # Refreshing the user to get the ID and default values (e.g. role):
        db.refresh(new_user)

        # Returning the new user (will be converted to the response model at the endpoints):
        return new_user

    except IntegrityError as e:
        # Rolling back the changes:
        db.rollback()

        # "from e" indicates that the current value error was caused by another error "e" (exception chaining):
        raise HTTPException(status_code=st.HTTP_409_CONFLICT, detail="User could not be created. Try logging in instead.") from e