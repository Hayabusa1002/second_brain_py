# app/core/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://user:password@localhost/second_brain"

    class Config:
        env_file = ".env"

settings = Settings()