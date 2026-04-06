import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


# 1. Grab the environment variable from Docker
DATABASE_URL = os.getenv("DATABASE_URL")

# 2. Create the engine (The physical connection)
engine = create_engine(DATABASE_URL)

# 3. Create a Session factory (The workspace for our queries)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. Create the Base class for our models to inherit from
Base = declarative_base()
