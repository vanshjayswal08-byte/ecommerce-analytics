# app/core/database.py
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.core.config import settings

# Create Async Engine
engine = create_async_engine(
    settings.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://"),
    echo=False,
    future=True,
    pool_size=20,
    max_overflow=10
)

# Create async session factory (Ye Pylance/Type errors ko fix karega)
AsyncSessionLocal = async_sessionmaker(
    bind=engine, 
    expire_on_commit=False
)

# Dependency to get DB session
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()