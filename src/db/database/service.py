from db.database.database import engine, Base
from logger.logs import logger


async def init_models():
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

            logger['info'].info(
                f"Database models have been successfully initialized"
            )
    except Exception as exc:
        logger['error'].error(
            f"Error initializing database models:\n{repr(exc)}"
        )
