
from pydantic-settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    genderise_api: str = ""
    cors_origins: list[str] = ["*"]

@lru_cache
def get_settings() -> Settings:
    return Settings()

settings = get_settings()


