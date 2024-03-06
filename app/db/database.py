__all__ = 'engine', 'SessionLocal', 'Base'

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine, AsyncAttrs
from sqlalchemy.ext.asyncio import async_sessionmaker

from app.configs import config


engine = create_async_engine(
    url=config.db.url,
    connect_args={"check_same_thread": False},
    echo=True
)

SessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass
