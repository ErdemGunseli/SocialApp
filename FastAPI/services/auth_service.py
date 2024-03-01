from fastapi import HTTPException, status as st

from dependencies import db_dependency, auth_dependency
from models import User
from security import bcrypt_context, create_access_token


def authenticate_user(email: str, password: str, db: db_dependency) -> User:
    # Searching for a user of the given id:
    user = db.query(User).filter((User.email == email)).first()
    if user is None:
        raise HTTPException(status_code=st.HTTP_404_NOT_FOUND, detail="User with this identifier is not found.")
    elif not bcrypt_context.verify(password, user.password):
        raise HTTPException(status_code=st.HTTP_401_UNAUTHORIZED, detail="Email or password incorrect")
    return user


def login_and_generate_token(user_input: auth_dependency, db: db_dependency) -> dict:
    # user_input is of type OAuth2PasswordRequestForm, so it has attributes username and password.
    # In this case, username represents the user's email:
    user = authenticate_user(user_input.username, user_input.password, db)

    # If the execution reaches this point, we know user is not None.
    token = create_access_token(user.id)

    # TODO: 2 tokens, a long-lived and used for refreshing, and a standard token for requests

    # 'bearer' indicates a request should be authenticated using the provided access token
    # i.e. it is a hint about how to use the token.
    # The return value uses the OATH2.0 Bearer Token Specification format:
    return {"access_token": token, "token_type": "bearer"}
    