from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Loading environment variables before local imports:
load_dotenv()

from services import post_service as ps
from routers import users, posts, auth
from config import read_config
from database import engine
import models

app = FastAPI()


# Creating all the tables represented by the models using the engine.
# The database URL was used when creating the engine.
# This will only be run if the database doesn't already exist.
models.Base.metadata.create_all(bind=engine)

# Stating that the auth.py file is a sub-application of the main application:
# Need to do this for each router that we want to use in the application:
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(posts.router)


# Mounting for the static post_images file:
app.mount(f"/{ps.IMAGE_DIRECTORY}", StaticFiles(directory=ps.IMAGE_DIRECTORY), name=ps.IMAGE_DIRECTORY)


# Cross-Origin Resource Sharing is a browser security feature, preventing malicious websites from accessing 
# data from another domain without permission. If we want our API to be accessible from web applications hosted
# on different domains, we need to add the domains that are permitted.

# The React front-end runs on port 3000:
origins = read_config("cors_origins")

# allow_credentials means authentication is allowed:
# '*' indicates all HTTP methods and headers are allowed:
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, 
                   allow_methods=['*'], allow_headers=['*'])

# TODO: Add HTTPS support
# TODO: Implement rate limiting with SlowAPI

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
