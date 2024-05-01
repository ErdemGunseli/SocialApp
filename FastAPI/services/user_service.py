import os

from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, File, UploadFile, status as st

from dependencies import user_dependency, db_dependency
from services.image_service import create_image
from services.auth_service import authenticate_user
from schemas import CreateUserRequest, UpdateUserRequest, UpdateUserPasswordRequest
from models import User, Image
from security import bcrypt_context


def create_user(db: db_dependency, user_data: CreateUserRequest) -> User:
    # Hashing the password:
    password_hash = bcrypt_context.hash(user_data.password)

    # Creating a new user instance with the hashed password instead of plaintext:
    new_user = User(**user_data.dict(exclude={"password"}), password=password_hash)

    try: 
        # Returning the new user (will be converted to the response model at the endpoints):
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
        
    except IntegrityError:
        raise HTTPException(status_code=st.HTTP_409_CONFLICT, detail="A user with this email already exists. Try logging in instead.")


def update_user(db: db_dependency, user: user_dependency, user_data: UpdateUserRequest) -> User:
    try:
        for key, value in user_data.dict().items():
            setattr(user, key, value)

        db.commit()

        return user
        
    except IntegrityError:
        raise HTTPException(status_code=st.HTTP_409_CONFLICT, detail="A user with this email already exists. Try logging in instead.")
    

def update_user_password(db: db_dependency, user: user_dependency, password_data: UpdateUserPasswordRequest) -> None:

    authenticate_user(db, user.email, password_data.old_password)

    # Hashing the password:
    password_hash = bcrypt_context.hash(password_data.new_password)
    user.password = password_hash
    db.commit()


async def create_profile_image(db: db_dependency, user: user_dependency, image: UploadFile = File(...)) -> Image:
    path = await create_image(image)
    image_record = Image(user_id=user.id, path=path)
    db.add(image_record)
    db.commit()

    return image_record


def read_profile_image(db: db_dependency, user_id: int) -> Image:
    image = db.query(Image).filter(Image.user_id == user_id).first()

    if image is None: raise HTTPException(status_code=st.HTTP_404_NOT_FOUND, detail="No profile image")
    return image


def delete_profile_image(db: db_dependency, user: user_dependency) -> None:
    # Deletes both the database record and actual image:
    image = db.query(Image).filter(Image.user_id == user.id).first()

    if image is None: raise HTTPException(status_code=st.HTTP_404_NOT_FOUND, detail="No profile image")

    if os.path.exists(image.path): os.remove(image.path)

    db.delete(image)
    db.commit()