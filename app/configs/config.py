from pydantic import BaseModel, Field

from app.configs.config_loader import load_active_settings


class Server(BaseModel):
    env_name: str
    port: int


class TGBot(BaseModel):
    token: str


class Database(BaseModel):
    url: str


class Config(BaseModel):
    server: Server
    tg_bot: TGBot
    db: Database


__unsafe_settings = load_active_settings()

config = Config(**__unsafe_settings)
