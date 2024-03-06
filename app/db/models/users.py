from sqlalchemy import Column, ForeignKey, String, Integer
from sqlalchemy.orm import relationship, Mapped, mapped_column
from uuid import uuid4

from datetime import datetime, UTC

from app.db.database import Base


class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(nullable=False)
    first_name: Mapped[str] = mapped_column(nullable=True)
    last_name: Mapped[str] = mapped_column(nullable=True)
    registration_name: Mapped[str] = mapped_column(nullable=False)
    connection_time: Mapped[str] = mapped_column(default=datetime.now(UTC))


class UserLessonRegistrationProcess(Base):
    __tablename__ = "user_lesson_registration_process"

    object_id: Mapped[str] = mapped_column(primary_key=True, default=uuid4)
    user_id: Mapped[str] = mapped_column(ForeignKey('users.id'))
    chat_id: Mapped[str] = mapped_column(nullable=False)
    message_id: Mapped[str] = mapped_column(nullable=False)
    status: Mapped[str] = mapped_column(nullable=False)

    user: Mapped["Users"] = relationship()

