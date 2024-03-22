__all__ = ("LessonReg",)

from pydantic import Field
from .lesson_reg_process import LessonRegProcess


class LessonReg(LessonRegProcess):
    date: str | None = Field(serialization_alias="Дата урока")
    username: str = Field(serialization_alias="Телега")
    type: str | None = Field(serialization_alias="Тип урока")
    registration_name: str = Field(serialization_alias="Имя")
    place: str | None = Field(serialization_alias="Место урока")
    number: str | None = Field(serialization_alias="Номер урока")
    listened_to_theory: str = Field(
        alias="need_theory", serialization_alias="Нужна теория"
    )
    start_time: str | None = Field(serialization_alias="Желаемое время")
    instructor: str | None = Field(serialization_alias="Желаемый инструктор")
    comment: str | None = Field(serialization_alias="Комментарий")
