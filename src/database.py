from config import REDIS_HOST, REDIS_DB, REDIS_PORT, DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER

import redis.asyncio as redis
from aredis_om import get_redis_connection

from typing import AsyncGenerator

from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool


DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
REDIS_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"

Base = declarative_base()

metadata = MetaData()

engine = create_async_engine(DATABASE_URL, poolclass=NullPool)
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


redis_connection = get_redis_connection(url=REDIS_URL)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


async def get_pipeline_session() -> AsyncGenerator[redis.client.Pipeline, None]:
    async with redis_connection.pipeline(transaction=True) as pipe:
        yield pipe


async def get_pubsub_session() -> AsyncGenerator[redis.client.PubSub, None]:
    async with redis_connection.pubsub() as pubsub:
        yield pubsub
