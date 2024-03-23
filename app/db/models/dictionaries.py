__all__ = (
    "LessonTypeDb",
    "LessonPlaceDb",
    "LessonInstructorDb",
)

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, MetaData
from sqlalchemy.ext.declarative import DeferredReflection
from sqlalchemy.orm import relationship, Mapped, mapped_column, declared_attr

from app.db.base import Base
from app.funcs import str_datetime

from .users import UserDb


class DictionaryDb(Base):
    __abstract__ = True

    object_id: Mapped[int] = mapped_column(
        primary_key=True, unique=True, autoincrement=True
    )
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    updated_at: Mapped[str] = mapped_column(nullable=False, default=str_datetime)
    updated_user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=True)

    if TYPE_CHECKING:
        updated_user: Mapped[UserDb]
    else:
        @declared_attr
        def user(self) -> Mapped["UserDb"]:
            return relationship(lazy="select")

    def __repr__(self):
        return (
            f"\n=========================="
            f"\nИдентификатор - {self.object_id}"
            f"\nНаименование - {self.name}"
            f"\nДата обновления - {self.updated_at}"
            f"\nКем обновлено - {"@" + self.user.username if self.user else 'нет данных'}"
        )


class LessonTypeDb(DictionaryDb):
    __tablename__ = "lessons_types"


class LessonPlaceDb(DictionaryDb):
    __tablename__ = "lessons_places"


class LessonInstructorDb(DictionaryDb):
    __tablename__ = "lessons_instructors"
