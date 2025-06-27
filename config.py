from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import computed_field


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_DB: str
    REDIS_PASS: str

    JWT_SECRET_KEY: str
    JWT_ENCODE_ALGORITHM: str
    JWT_EXPIRE_DAYS: int

    GOOGLE_CLIENT_ID: str
    GOOGLE_PROJECT_ID: str
    GOOGLE_AUTH_URI: str
    GOOGLE_TOKEN_URI: str
    GOOGLE_CLIENT_SECRET: str
    GOOGLE_REDIRECT_URI: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

    @computed_field
    @property
    def redis_url(self) -> str:
        if self.REDIS_PASS:
            return f"redis://:{self.REDIS_PASS}@" \
                   f"{self.REDIS_HOST}:" \
                   f"{self.REDIS_PORT}/" \
                   f"{self.REDIS_DB}"
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"

    @computed_field
    @property
    def db_url_asyncpg(self) -> str:
        return (
            f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    @computed_field
    @property
    def db_url_psycopg2(self) -> str:
        return (
            f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASS}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    @computed_field
    @property
    def google_redirect_url(self) -> str:
        return (f"{self.GOOGLE_AUTH_URI}?response_type=code"
                f"&client_id={self.GOOGLE_CLIENT_ID}"
                f"&redirect_uri={self.GOOGLE_REDIRECT_URI}"
                f"&scope=openid%20profile%20email&access_type=offline")


settings = Settings()
