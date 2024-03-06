from pydantic import BaseModel


class UserBase(BaseModel):
    id: int
    username: str
    first_name: str | None
    last_name: str | None
    registration_name: str


class UserCreate(UserBase):
    pass


class User(UserBase):
    connection_time: str
