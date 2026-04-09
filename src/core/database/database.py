__all__ = ["Database"]

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from core.env import env

from .models import Base


class Database:
    """Высокоуровневая обертка над взаимодействием с базой данных."""

    engine: AsyncEngine = create_async_engine(url=env.postgres_dsn)
    """Предварительно инициализированный движок базы данных."""

    sessionmaker = async_sessionmaker(bind=engine)
    """Фабрика асинхронных сессий."""

    def __init__(self, session: AsyncSession) -> None:
        """Создаёт экземпляр Database с переданной сессией.

        Args:
            session: Асинхронная сессия, используемая для операций с БД.

        """
        self.session: AsyncSession = session

    @classmethod
    @asynccontextmanager
    async def session_context(cls) -> AsyncGenerator["Database"]:
        """Асинхронный контекстный менеджер, предоставляющий сессию Database.

        Returns:
            Экземпляр Database с активной сессией.

        """
        async with cls.sessionmaker() as session:
            yield cls(session)

    async def commit(self) -> None:
        """Фиксирует изменения текущей сессии в базе данных."""
        await self.session.commit()

    async def refresh(self, instance: type[Base]) -> None:
        """Обновляет атрибуты экземпляра модели актуальными данными из БД.

        Args:
            instance: Экземпляр ORM-модели для обновления.

        """
        await self.session.refresh(instance)

    async def flush(self) -> None:
        """Сбрасывает изменения в БД без коммита (для получения autoincrement id и т.п.)."""
        await self.session.flush()
