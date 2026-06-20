from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from collections.abc import AsyncGenerator
from app.config import settings

engine = create_async_engine(
    settings.auth_db_url,
    pool_pre_ping=True
)

async_session = async_sessionmaker(
    engine,
    expire_on_commit=False
)

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session