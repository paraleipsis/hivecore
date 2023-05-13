from db.database.database import engine, Base
from logger.logs import logger


async def init_models():
    try:
        async with engine.begin() as conn:
            print(Base.metadata.tables.values())
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

            logger['info'].info(
                "Database models have been successfully initialized"
            )
    except Exception as exc:
        logger['error'].error(
            f"Error initializing database models:\n{repr(exc)}"
        )
