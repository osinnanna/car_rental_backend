from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", case_sensitive=True)

    DATABASE_URL: str
    API_PREFIX: str = "/api"
    DEBUG: bool = False
    SECRET_KEY: str = "fastcars-super-secure-secret-key-2026"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    ALLOWED_ORIGINS: str = ""

    @field_validator("ALLOWED_ORIGINS")
    def parse_allowed_origins(cls, v: str) -> list[str]:
        return v.split(",") if v else []


settings = Settings()
