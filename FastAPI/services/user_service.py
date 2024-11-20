import os

from sqlalchemy.exc import IntegrityError
from fastapi import File, UploadFile
from exceptions import UserNotFoundError, UserAlreadyExistsError, ImageNotFoundError

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
    new_user = User(**user_data.model_dump(exclude={"password", "name"}), name=user_data.name.title(), password=password_hash)

    try: 
        # Returning the new user (will be converted to the response model at the endpoints):
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
        
    except IntegrityError:
        raise UserAlreadyExistsError


def get_user(db: db_dependency, user_id: int) -> User:
    user = db.query(User).filter_by(id=user_id).first()

    # Ensuring the user exists:
    if user is None: raise UserNotFoundError
    
    user.profile_image_url = read_profile_image(db, user_id).url
    return user


def update_user(db: db_dependency, user: user_dependency, user_data: UpdateUserRequest) -> User:
    try:
        for key, value in user_data.dict().items():
            setattr(user, key, value)

        db.commit()

        return user
        
    except IntegrityError:
        raise UserAlreadyExistsError
    

def update_user_password(db: db_dependency, user: user_dependency, password_data: UpdateUserPasswordRequest) -> None:

    authenticate_user(db, user.email, password_data.old_password)

    # Hashing the password:
    password_hash = bcrypt_context.hash(password_data.new_password)
    user.password = password_hash
    db.commit()


async def create_profile_image(db: db_dependency, user: user_dependency, image: UploadFile = File(...)) -> Image:
    url = await create_image(image)
    image_record = Image(user_id=user.id, url=url)
    db.add(image_record)
    db.commit()

    return image_record


def read_profile_image(db: db_dependency, user_id: int) -> Image:
    image = db.query(Image).filter_by(user_id=user_id).first()

    if image is None: raise ImageNotFoundError
    return image


def delete_profile_image(db: db_dependency, user: user_dependency) -> None:
    # Deletes both the database record and actual image:
    image = db.query(Image).filter_by(user_id=user.id).first()

    if image is None: raise ImageNotFoundError

    if os.path.exists(image.url): os.remove(image.url)

    db.delete(image)
    db.commit()