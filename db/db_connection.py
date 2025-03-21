from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from fastapi import Depends
from typing import Annotated
import logging

logging.basicConfig(level=logging.INFO)
db_url = "postgresql+asyncpg://postgres:postgres@localhost:5432/itrium"

engine = create_async_engine(db_url)

async_session = async_sessionmaker(bind= engine, expire_on_commit=False)

async def get_db():
    try:
        async with async_session() as session:
            yield session
    except Exception as e:
        logging.info(f"Database connection error: {e}")
        
