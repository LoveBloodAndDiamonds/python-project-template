__all__ = ["Environment", "env"]


from pydantic import Field
from pydantic_settings import BaseSettings
from sqlalchemy import URL


class Environment(BaseSettings):
    """Переменные окружения приложения, считываемые из .env файла."""

    # Настройки логирования
    logging_stdout_level: str = Field(default="INFO")
    logging_file_level: str = Field(default="INFO")

    # Настройки админ панели
    app_port: int = Field(default=80)
    admin_password: str = Field(default="admin")

    # Ключ шифрования
    cypher_key: str

    # Настройки PostgreSQL
    database_driver: str = "asyncpg"
    database_system: str = "postgresql"
    postgres_user: str = Field(default="postgres")
    postgres_password: str = Field(default="")
    postgres_db: str = Field(default="")
    postgres_host: str = Field(default="postgres")
    postgres_port: int = Field(default=5432)

    @property
    def postgres_dsn(self) -> str:
        """Строка подключения к PostgreSQL в формате SQLAlchemy DSN.

        Returns:
            Строка вида ``postgresql+asyncpg://user:password@host:port/db``.

        """
        return URL.create(
            drivername=f"{self.database_system}+{self.database_driver}",
            username=self.postgres_user,
            database=self.postgres_db,
            password=self.postgres_password,
            port=self.postgres_port,
            host=self.postgres_host,
        ).render_as_string(hide_password=False)


env = Environment()  # type: ignore
"""Глобальный объект с переменными окружения."""
