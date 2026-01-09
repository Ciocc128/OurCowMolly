import os

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

# Database config
DATABASE_URL = "sqlite:///./data/ourcowmolly.db"
# ASYNC_DATABASE_URL = 

# Synch engine for migrations and intial setup
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# # Asynch engine for FastAPI
# async_engine = create_async_engine(ASYNC_DATABASE_URL)
# async_session = sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()

# helper functions they will be used in FastAPI routes to provide db sessions
def get_db():
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# async def get_async_db():
#     """Dependency to get async database session"""
#     async with async_session() as session:
#         yield session
