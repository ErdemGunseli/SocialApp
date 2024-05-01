from typing import Annotated, Optional

from fastapi import Depends, HTTPException, status as st
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import jwt, JWTError

from database import SessionLocal
from models import User
from security import HASH_SECRET_KEY, HASH_ALGORITHM
from enums import Role

# The following is a generator function - a special function that uses the yield keyword instead of return.
# Typically, generators are used to create iterators which produce a series of values,
# used in scenarios where it is necessary to generate a sequence of values dynamically,
# rather than generating the entire sequence upfront. The next value can be obtained from
# the iterator by calling the next method on it.

# In this case, we are using it to create a context manager.
# A context manager is a way of managing resources that need to be cleaned up after use
# i.e. a closing the database connection after it is no longer needed.

# When generators are used to produce iterators, the fact that the code stops after the yield keyword
# is used to repeatedly return values each time the next method is called.
# In this case, it is being used to keep the database connection open
# until the function that calls get_db completes after which the database can be closed.

def get_db():
    # Using the custom session class to connect to the database.
    # db represents a database connection.
    db = SessionLocal()
    try:
        # Returning the database connection that we just created.
        # Doing this using the "yield" keyword means that the database will not be closed too early.
        yield db
    
    except Exception:
        db.rollback()
        raise
    
    finally:
        # The code following the yield statement will only be run once the read_all function finishes.
        db.close()


# "Depends" relates to dependency injection - the execution of the relevant endpoints depend on the availability of a
# database connection.

# The argument of "Depends" specifies which function should be called for the dependency injection.
# When a function that depends on a db connection is called and needs a value for the db parameter, FastAPI will
# invoke the get_db function to obtain the database session as the value for the dependency.

# The Annotated class is from the typing module and allows us to add additional metadata to type hints.
# In this case, we are indicating that the database Session object is a dependency that should be injected into the
# function.

# Session, imported from SQLAlchemy is the type of the dependency - a database session.
db_dependency = Annotated[Session, Depends(get_db)]

# For the authentication dependency, the OAuth2PasswordRequestForm class must be instantiated:
auth_dependency = Annotated[OAuth2PasswordRequestForm, Depends(OAuth2PasswordRequestForm)]
# Instantiating OAuth2PasswordBearer with the token-generating endpoint URL as a kwarg:
token_dependency = Annotated[str, Depends(OAuth2PasswordBearer(tokenUrl="auth/token"))]


async def get_current_user(db: db_dependency, token: token_dependency) -> User:
    # Error catching in case token is invalid:
    try:
        # Attempting to decode the token using the secret key and algorithm:
        # If successful, this will return a dictionary that contains the user data:
        payload = jwt.decode(token, HASH_SECRET_KEY, algorithms=[HASH_ALGORITHM])

        # Extracting the user id from the payload dictionary:
        # The subject of a JWT needs to be a string, so converting back to integer:
        user_id: Optional[int] = int(payload.get("sub"))

    except JWTError as e:
        raise HTTPException(status_code=st.HTTP_401_UNAUTHORIZED, detail="Error When Decoding JWT") from e
    if user_id is None: raise HTTPException(status_code=st.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials")
    return get_user(user_id, db)


def get_user(user_id, db: db_dependency) -> User:
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=st.HTTP_404_NOT_FOUND, detail="User not found")
    return user


user_dependency = Annotated[dict, Depends(get_current_user)]


def verify_admin_status(user) -> None:
    # When interacting with the database models, we can use the enum directly, since the columns are of type Enum.
    # JWTs require all data to be JSON serializable, so we passed enum.value (the string equivalent of the enum).
    # Therefore, we need to compare it with enum.value:
    if user is None or user.get("role") != Role.ADMIN.value:
        raise HTTPException(status_code=st.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials")


async def get_current_admin(token: token_dependency) -> User:
    # Need to use await, since it is an async function:
    user = await get_current_user(token)
    verify_admin_status(user)
    return user

admin_dependency = Annotated[dict, Depends(get_current_admin)]