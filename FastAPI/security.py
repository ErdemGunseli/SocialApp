import os
from datetime import datetime, timedelta, timezone

from fastapi import File, UploadFile
from passlib.context import CryptContext
from jose import jwt


# Indicating that we want to use the bcrypt hashing algorithm:
# Setting deprecated to "auto" means that any password hashes that are not using bcrypt will be automatically updated:
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# A JWT needs an algorithm and secret key:
# Secret key should be a random string. This was generated using openssl rand -hex 32:
# It is stored as a persistent environment variable, using .env:

HASH_SECRET_KEY = os.getenv("HASH_SECRET_KEY")
HASH_ALGORITHM = os.getenv("HASH_ALGORITHM")
# The time to live for the JWT:
TOKEN_TTL = timedelta(minutes=int(os.getenv("TOKEN_TTL")))


def create_access_token(user_id: int, ttl: timedelta = TOKEN_TTL) -> str:
    expiry = datetime.now(timezone.utc) + ttl
    
    # The payload is the data that we want to encode within the token.
    # Tokens will be used by the server to understand which user is making the requests.
    # "sub" stands for the subject, and should be unique.
    # Excluding email since it is sensitive.
    # Role checks will be done through the database, tokens have a ttl and if an admin is downgraded during that time, 
    # they would still be able to perform admin actions until the token is refreshed if the role was stored in the token:
    payload = {"sub": str(user_id), "exp": expiry}

    # Creating the JWT, using the secret key and algorithm to encode the payload:
    return jwt.encode(payload, HASH_SECRET_KEY, HASH_ALGORITHM)


def check_for_malware(image: UploadFile = File(...)):
    # TODO: Malware scanning with ClamAV
    # TODO: Check for size (large files should not be uploaded)
    # If check fails, raise exception.
    pass

