__all__ = ("db_helper",)

from asyncio import current_task

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    async_scoped_session,
    AsyncSession,
)

from app.configs import config


class DBHelper:
    def __init__(self, url: str, echo: bool = False):
        self.engine = create_async_engine(
            url=url,
            connect_args={"check_same_thread": False},
            echo=echo,
        )
        self.session_factory = async_sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine, expire_on_commit=False
        )


db_helper = DBHelper(
    url=config.db.url,
    echo=config.db.echo,
)
