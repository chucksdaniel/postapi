from pathlib import Path
from pydantic_settings import BaseSettings
from pydantic import ConfigDict

BASE_DIR = Path(__file__).resolve().parent

class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    # class Config:
    #     env_file = ".env"
    model_config = ConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8"
    )
    # To run the server with the specified env file:
    # uvicorn postapi.app:app --reload --env-file postapi/.env

settings = Settings()