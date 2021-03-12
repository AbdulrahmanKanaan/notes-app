from functools import lru_cache
from pydantic.env_settings import BaseSettings

class Settings(BaseSettings):

    APP_NAME: str

    DB_HOST: str
    DB_PORT: str
    DB_DATABASE: str
    DB_USERNAME: str
    DB_PASSWORD: str

    SECERET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    class Config:
        env_file=".env"

@lru_cache()
def get_settings() -> Settings:
    return Settings()