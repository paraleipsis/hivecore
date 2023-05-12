from db.storage_config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER

from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool


DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

Base = declarative_base()

metadata = MetaData()

engine = create_async_engine(
    url=DATABASE_URL,
    poolclass=NullPool
)

# noinspection PyTypeChecker
async_session_maker = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)
