__all__ = ("config",)

from pydantic import BaseModel, Field

from app.configs.config_loader import load_active_settings


class Server(BaseModel):
    env_name: str
    port: int


class TimeLimit(BaseModel):
    hours: str
    minutes: str


class Registration(BaseModel):
    timelimit: TimeLimit


class TGBot(BaseModel):
    token: str
    registration: Registration


class Database(BaseModel):
    url: str
    echo: bool


class Config(BaseModel):
    server: Server
    tg_bot: TGBot
    db: Database


__unsafe_settings = load_active_settings()

config = Config(**__unsafe_settings)
