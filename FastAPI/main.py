import os

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from dotenv import load_dotenv

# Loading environment variables before local imports:
load_dotenv()

# Declaring FastAPI instance before local imports to avoid circular imports:
app = FastAPI()

# Rate limiting with SlowAPI:
# key_func kwarg takes in a function that returns a unique key for the client (here we are using a function to get the IP address):
# default_limits apply to all endpoints unless overridden by a decorator.
limiter = Limiter(key_func=get_remote_address, default_limits=["3/second", "120/minute"])
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

from services import image_service as imgs
from routers import auth, posts, users
from config import read_config
from database import engine
import models


# Creating all the tables represented by the models using the engine.
# The database URL was used when creating the engine.
# This will only be run if the database doesn't already exist.
models.Base.metadata.create_all(bind=engine)

# Stating that the auth.py file is a sub-application of the main application:
# Need to do this for each router that we want to use in the application:
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(posts.router)

# Creating the static images folder, but not raising an error if it already exists:
os.makedirs(imgs.IMAGE_DIRECTORY, exist_ok=True)

# Mounting the static post_images folder:
app.mount(f"/{imgs.IMAGE_DIRECTORY}", StaticFiles(directory=imgs.IMAGE_DIRECTORY), name=imgs.IMAGE_DIRECTORY)


# Cross-Origin Resource Sharing is a browser security feature, preventing malicious websites from accessing 
# data from another domain without permission. If we want our API to be accessible from web applications hosted
# on different domains, we need to add the domains that are permitted.
origins = read_config("cors_origins")

# allow_credentials means authentication is allowed:
# '*' indicates all HTTP methods and headers are allowed:
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, 
                   allow_methods=['*'], allow_headers=['*'])


# Alembic is a lightweight database migration tool for SQLAlchemy (version control for DB schema).
# It helps manage real-time migrations - changes to the db schema (structures and connections within tables).
# It provides scripts to generate migrations, apply them to the db, and roll back if needed.
# alembic init <folder_name> - creates a new environment with the necessary files to use Alembic.
# alembic revision -m <message> - creates a new migration script.
# alembic upgrade <revision#> - applies the migration to the db.
# alembic downgrade <revision#> - rolls back the migration.


"""
cd FastAPI
source venv/bin/activate
uvicorn main:app --reload
"""
