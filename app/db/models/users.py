from sqlalchemy import Column, ForeignKey, String, Integer
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.sql import func

from uuid import uuid4

from datetime import datetime, UTC

from app.db.base import Base


def str_datetime():
    return str(datetime.now(UTC))


class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(nullable=False)
    first_name: Mapped[str] = mapped_column(nullable=True)
    last_name: Mapped[str] = mapped_column(nullable=True)
    registration_name: Mapped[str] = mapped_column(nullable=False)
    is_admin: Mapped[bool] = mapped_column(nullable=False, default=False)
    updated_at: Mapped[str] = mapped_column(nullable=False)
    connected_at: Mapped[str] = mapped_column(nullable=False, default=str_datetime)

    def __repr__(self):
        return (
            f"\n================================================"
            f"\nИдентификатор - {self.id}"
            f"\nТелега - @{self.username}"
            f"\nИмя - {self.first_name}"
            f"\nФамилия - {self.last_name}"
            f"\nИмя для уроков - {self.registration_name}"
            f"\nАдмин - {self.is_admin}"
            f"\nЗапись обновлена - {self.updated_at}"
            f"\nДата регистрации - {self.connected_at}\n\n"
        )


class UserLessonRegistrationProcess(Base):
    __tablename__ = "user_lesson_registration_process"

    object_id: Mapped[str] = mapped_column(primary_key=True, default=uuid4)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"))
    chat_id: Mapped[str] = mapped_column(nullable=False)
    message_id: Mapped[str] = mapped_column(nullable=False)
    status: Mapped[str] = mapped_column(nullable=False)

    user: Mapped["Users"] = relationship()
