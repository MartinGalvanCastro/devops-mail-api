from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_TITLE: str = "Mail API"
    APP_VERSION: str = "0.1.0"

    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"

    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "postgres"
    DB_NAME: str = "mail_db"
    DB_DRIVER: str = "postgresql+psycopg"

    JWT_SECRET_KEY: str = "secretkey"

    @property
    def DB_URL(self) -> str:
        return f"{self.DB_DRIVER}://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def DB_URL_TEST(self) -> str:
        return f"{self.DB_DRIVER}://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}_test"

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8", "extra": "ignore"}


settings: Settings = Settings()
