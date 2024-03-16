__all__ = (
    "LessonTypeDb",
    "LessonPlaceDb",
    "LessonInstructorDb",
)

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from uuid import uuid4

from app.db.base import Base
from app.funcs import str_datetime

from .users import UserDb


class LessonTypeDb(Base):
    __tablename__ = "lessons_types"

    object_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    updated_at: Mapped[str] = mapped_column(nullable=False, default=str_datetime)
    updated_user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    user: Mapped["UserDb"] = relationship()


class LessonPlaceDb(Base):
    __tablename__ = "lessons_places"

    object_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    updated_at: Mapped[str] = mapped_column(nullable=False, default=str_datetime)
    updated_user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    user: Mapped["UserDb"] = relationship()


class LessonInstructorDb(Base):
    __tablename__ = "lessons_instructors"

    object_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    updated_at: Mapped[str] = mapped_column(nullable=False, default=str_datetime)
    updated_user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    user: Mapped["UserDb"] = relationship()
