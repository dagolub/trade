import secrets
from typing import Any, Dict, Optional
from pydantic import AnyHttpUrl, BaseSettings, EmailStr, HttpUrl, validator


class Settings(BaseSettings):
    API_V1_STR: str = "/api"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8

    SERVER_NAME: str
    SERVER_HOST: AnyHttpUrl
    PROJECT_NAME: str

    FIRST_SUPERUSER: EmailStr
    FIRST_SUPERUSER_PASSWORD: str

    EMAIL_TEMPLATES_DIR: str = "app/email-templates/build"
    EMAILS_FROM_EMAIL: Optional[EmailStr] = None
    EMAILS_FROM_NAME: Optional[str] = None

    @validator("EMAILS_FROM_NAME")
    def get_project_name(cls, v: Optional[str], values: Dict[str, Any]) -> str:
        return v or values["PROJECT_NAME"]

    EMAIL_RESET_TOKEN_EXPIRE_HOURS: int = 48
    EMAIL_TEST_USER: EmailStr = "info@pdfmax.xyz"  # type: ignore

    SMTP_HOST: Optional[str] = None
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    SMTP_PORT: Optional[int] = None
    SMTP_TLS: bool = True

    MONGO_HOST: str
    MONGO_USER: str
    MONGO_PASS: str
    MONGO_DB: str
    MONGO_PORT = 27017

    SENTRY_DSN: Optional[HttpUrl] = None

    @validator("SENTRY_DSN", pre=True)
    def sentry_dsn_can_be_blank(cls, v: str) -> Optional[str]:
        return v or None

    ENVIRONMENT: str

    FILES_HOST: str
    FILES_KEY: str = None
    FILES_SECRET: str = None

    class Config:
        case_sensitive = True


settings = Settings()  # type: ignore
