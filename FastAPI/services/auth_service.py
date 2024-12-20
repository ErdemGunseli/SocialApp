from dependencies import db_dependency, auth_dependency
from models import User
from security import bcrypt_context, create_access_token
from exceptions import UserNotFoundError, PasswordVerificationError


def authenticate_user(db: db_dependency, email: str, password: str) -> User:
    # Searching for a user of the given email:
    user = db.query(User).filter_by(email=email).first()

    if user is None:
        raise UserNotFoundError
    elif not bcrypt_context.verify(password, user.password):
        raise PasswordVerificationError
    return user


def login_and_generate_token(db: db_dependency, auth_form: auth_dependency) -> dict:
    # auth_form is of type OAuth2PasswordRequestForm, so it has attributes username and password.
    # In this case, username represents the user's email:
    user = authenticate_user(db, auth_form.username, auth_form.password)

    # If the execution reaches this point, we know user is not None.
    token = create_access_token(user.id)

    # TODO: 2 tokens, a long-lived and used for refreshing, and a standard token for requests

    # 'bearer' indicates a request should be authenticated using the provided access token
    # i.e. it is a hint about how to use the token.
    # The return value uses the OATH2.0 Bearer Token Specification format:
    return {"access_token": token, "token_type": "bearer"}