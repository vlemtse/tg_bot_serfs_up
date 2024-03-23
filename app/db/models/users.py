__all__ = ("UserDb",)

from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.funcs import str_datetime


class UserDb(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(nullable=False)
    first_name: Mapped[str] = mapped_column(nullable=True)
    last_name: Mapped[str] = mapped_column(nullable=True)
    registration_name: Mapped[str] = mapped_column(nullable=False)
    is_bot_admin: Mapped[bool] = mapped_column(nullable=False, default=False)
    is_reg_admin: Mapped[bool] = mapped_column(nullable=False, default=False)
    chat_id: Mapped[int] = mapped_column(nullable=True)
    updated_at: Mapped[str] = mapped_column(nullable=False)
    connected_at: Mapped[str] = mapped_column(nullable=False, default=str_datetime)

    def __repr__(self):
        return (
            f"\n=========================="
            f"\nИдентификатор - {self.id}"
            f"\nТелега - @{self.username}"
            f"\nИмя - {self.first_name}"
            f"\nФамилия - {self.last_name}"
            f"\nИмя для уроков - {self.registration_name}"
            f"\nАдмин бота - {self.is_bot_admin}"
            f"\nАдмин регистрации - {self.is_reg_admin}"
            f"\nЗапись обновлена - {self.updated_at}"
            f"\nДата регистрации - {self.connected_at}\n\n"
        )
