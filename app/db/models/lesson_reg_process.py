from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from uuid import uuid4

from app.db.base import Base
from app.funcs import str_datetime, str_uuid4

from .users import Users


class UserLessonRegistrationProcess(Base):
    __tablename__ = "user_lesson_registration_process"

    object_id: Mapped[str] = mapped_column(primary_key=True, default=str_uuid4)
    # todo UK(user_id + chat_id + message_id)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    chat_id: Mapped[int] = mapped_column(nullable=False)
    message_id: Mapped[int] = mapped_column(nullable=False)
    state: Mapped[str] = mapped_column(nullable=True)
    status: Mapped[str] = mapped_column(nullable=False)
    updated_at: Mapped[str] = mapped_column(nullable=False, default=str_datetime)

    user: Mapped["Users"] = relationship()
