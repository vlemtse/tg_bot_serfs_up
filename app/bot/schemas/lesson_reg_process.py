__all__ = ("LessonRegProcess",)

from pydantic import BaseModel, Field


class LessonRegProcess(BaseModel):
    type: str | None = Field(default=None)
    date: str | None = Field(default=None)
    number: str | None = Field(default=None)
    place: str | None = Field(default=None)
    start_time: str | None = Field(default=None)
    instructor: str | None = Field(default=None)
