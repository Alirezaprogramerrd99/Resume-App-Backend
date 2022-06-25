from functools import lru_cache
from typing import Any, Dict, Optional
from pydantic import BaseSettings, PostgresDsn, validator
import os
from pathlib import Path


class Settings(BaseSettings):
    PROJECT_NAME: str = "Resume App"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    USERS_OPEN_REGISTRATION: str

    ENVIRONMENT: Optional[str]
    BASE_DIR = Path(__file__).resolve().parent.parent.parent
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

    FIRST_ADMIN_EMAIL: str
    FIRST_ADMIN_PASSWORD: str

    DB_HOST: str
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str

    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    # SENTRY_DSN: str

    S3_HOST: str
    S3_API_PORT: str
    S3_CONSOLE_PORT: str
    S3_ROOT_USER: str
    S3_ROOT_PASSWORD: str
    S3_PROFILE_BUCKET: str

    SERVER_ADDRESS: str

    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_PORT: int
    MAIL_SERVER: str
    MAIL_FROM_NAME: str

    REDIS_HOST: str
    REDIS_PORT: str

    FORGET_PASSWORD_CODE_EXPIRATION: int

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(
        cls, v: Optional[str], values: Dict[str, Any]
    ) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("DB_USER"),
            password=values.get("DB_PASSWORD"),
            host=values.get("DB_HOST"),
            path=f"/{values.get('DB_NAME') or  ''}",
        )

    class Config:
        case_sensitive = True
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()
