from click import echo
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from core.configs import settings

engine = create_async_engine(
    settings.DB_URL,
    pool_size=10,
    max_overflow=20,
    pool_timeout=30,
    pool_pre_ping=True,
    echo=False
)
Session = async_sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
    class_=AsyncSession,
)
