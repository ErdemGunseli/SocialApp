# SQLAlchemy allows us to interact with databases using an OOP approach,
# providing object-relational mapping (ORM) that allows us to define Python classes
# (called models) that map to database tables.
from sqlalchemy import create_engine

# Session maker is a class that is used to create session objects for database interactions.
# These represent a connection to the database and provide a way to interact with the database.
from sqlalchemy.orm import sessionmaker

# The declarative_base function is used to create a base class for all data models.
# The data models will inherit from this class.
from sqlalchemy.ext.declarative import declarative_base

# Only network-based RDBMS require superusers. SQLite is file based:
# TODO: Switch to postgres and make db related functions async, and await when calling (AsyncSession)
import os
DB_URI = os.getenv("DB_URI")


# A database engine is a way of connecting the database.
# The function creates an instance of the Engine class, which acts as an intermediary between the Python code
# and the database, handling tasks such as connection management, SQL execution and result fetching.
# The create_engine function is used to establish a connection to the database.
# taking in the URL of the database within the application as well as "connection arguments" kwargs
# which specify additional requirements that should be passed to the underlying database connection.

engine = create_engine(DB_URI)

# Creating a custom session class bound to the engine.
# auto commit = False means that the database will not automatically commit changes, manual commits are required.
# auto flush = False means that the session's changes to the database won't be synchronised automatically
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Calling the declarative base function will return a new base class from which all data models inherit.
Base = declarative_base()


