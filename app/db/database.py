from core import settings

DATABASE_URL = settings.database_url

from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, create_async_engine

async_engine = create_async_engine(DATABASE_URL, echo=True)

# Настраиваем фабрику сеансов
async_session_factory = async_sessionmaker(
    async_engine,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


async def get_async_session() -> AsyncSession:
    async with async_session_factory() as async_session:
        yield async_session
