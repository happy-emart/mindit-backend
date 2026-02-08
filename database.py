import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()

# Use the pooling URL from Supabase Settings -> Database -> Connection Pooling
# Format: postgresql+asyncpg://[user]:[password]@[host]:6543/[db_name]?pgbouncer=true
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    # Fallback or error if not set. Warning for local dev.
    print("WARNING: DATABASE_URL not set in environment.")

engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    pool_pre_ping=True,
    pool_size=20,
    max_overflow=10
)

AsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

Base = declarative_base()

async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
