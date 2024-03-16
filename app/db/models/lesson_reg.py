__all__ = ("UserLessonRegistrationDb",)

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.db.base import Base
from app.funcs import str_datetime, str_uuid4

from .users import UserDb


class UserLessonRegistrationDb(Base):
    __tablename__ = "user_lesson_registrations"

    object_id: Mapped[str] = mapped_column(primary_key=True, default=str_uuid4)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    type: Mapped[str] = mapped_column(nullable=False)
    date: Mapped[str] = mapped_column(nullable=False)
    number: Mapped[str] = mapped_column(nullable=False)
    place: Mapped[str] = mapped_column(nullable=False)
    need_theory: Mapped[bool] = mapped_column(nullable=False)
    start_time: Mapped[str] = mapped_column(nullable=False)
    instructor: Mapped[str] = mapped_column(nullable=False)
    comment: Mapped[str] = mapped_column(nullable=True)
    created_at: Mapped[str] = mapped_column(nullable=False, default=str_datetime)

    user: Mapped["UserDb"] = relationship()
