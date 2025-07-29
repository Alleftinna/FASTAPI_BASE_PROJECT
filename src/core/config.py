
from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Application settings
    APP_NAME: str
    DEBUG: bool = False
    COMPOSE_PROFILES: str = "DEV"
    HOST_PORT: int = 8081

    # DB settings
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    DB_PORT: int
    DATABASE_ECHO: bool

    # Logging settings
    SQL_LOG_LEVEL: str = "INFO"  # DEBUG, INFO, WARNING, ERROR
    SQL_LOG_TO_CONSOLE: bool = False  # Отключаем SQL логи в консоли по умолчанию
    SQL_LOG_TO_FILE: bool = True  # Включаем SQL логи в файл по умолчанию
    
    @property
    def database_echo(self) -> bool:
        """Преобразует строковое значение DEBUG в bool"""
        return str(self.DATABASE_ECHO).lower() in ["True", "true", "1"]

    @property
    def debug_enabled(self) -> bool:
        """Преобразует строковое значение DEBUG в bool"""
        return str(self.DEBUG).lower() in ["True", "true", "1"]
    
    @property
    def async_database_url(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:5432/{self.DB_NAME}"

    @property
    def DB_HOST(self):
        return f"{self.APP_NAME}_db"


settings = Settings()