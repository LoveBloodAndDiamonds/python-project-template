__all__ = ["Repository"]

from collections.abc import Sequence
from typing import Any, TypeVar

from sqlalchemy import ColumnElement, delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import Base

AbstractModel = TypeVar("AbstractModel", bound=Base)


class Repository[AbstractModel]:
    """Базовый абстрактный репозиторий."""

    def __init__(self, type_model: type[AbstractModel], session: AsyncSession):
        """Инициализирует репозиторий для работы с указанной моделью.

        Args:
            type_model: ORM-класс модели, с которой работает репозиторий.
            session: Асинхронная сессия SQLAlchemy.

        """
        self.type_model = type_model
        self.session = session

    async def get(self, ident: int | str) -> AbstractModel | None:
        """Возвращает одну запись по первичному ключу.

        Args:
            ident: Значение первичного ключа.

        Returns:
            Найденный экземпляр модели или None, если запись отсутствует.

        """
        return await self.session.get(entity=self.type_model, ident=ident)

    async def get_by_where(self, whereclause: ColumnElement[bool]) -> AbstractModel | None:
        """Возвращает одну запись по условию.

        Args:
            whereclause: Условие фильтрации (например, ``Model.id == 1``).

        Returns:
            Найденный экземпляр модели или None, если совпадений нет.

        """
        statement = select(self.type_model).where(whereclause)
        result = await self.session.execute(statement)
        row = result.one_or_none()
        return row[0] if row else None

    async def get_many(
        self,
        whereclause: ColumnElement[bool] | None = None,
        limit: int = 999,
        order_by: Any | None = None,
    ) -> Sequence[AbstractModel]:
        """Возвращает несколько записей с фильтрацией, лимитом и сортировкой.

        Args:
            whereclause: Условие фильтрации. Если None — фильтр не применяется.
            limit: Максимальное количество возвращаемых записей.
            order_by: Выражение для сортировки (например, ``Model.created_at.desc()``).

        Returns:
            Последовательность найденных экземпляров модели.

        """
        statement = select(self.type_model)
        if whereclause is not None:
            statement = statement.where(whereclause)
        if limit:
            statement = statement.limit(limit)
        if order_by is not None:
            statement = statement.order_by(order_by)

        return (await self.session.scalars(statement)).all()

    async def get_all(
        self, whereclause: ColumnElement[bool] | None = None, order_by: Any | None = None
    ) -> Sequence[AbstractModel]:
        """Возвращает все записи без лимита, опционально с фильтром и сортировкой.

        Args:
            whereclause: Условие фильтрации. Если None — возвращаются все записи.
            order_by: Выражение для сортировки.

        Returns:
            Последовательность всех найденных экземпляров модели.

        """
        statement = select(self.type_model)
        if whereclause is not None:
            statement = statement.where(whereclause)
        if order_by is not None:
            statement = statement.order_by(order_by)

        return (await self.session.scalars(statement)).all()

    async def delete(self, whereclause: ColumnElement[bool]) -> None:
        """Удаляет записи, соответствующие условию.

        Args:
            whereclause: Условие для выборки удаляемых записей.

        """
        statement = delete(self.type_model).where(whereclause)
        await self.session.execute(statement)

    async def delete_all(self) -> None:
        """Удаляет все записи модели из таблицы."""
        statement = delete(self.type_model)
        await self.session.execute(statement)
