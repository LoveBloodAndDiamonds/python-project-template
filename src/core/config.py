__all__ = ["config", "Configuration"]

from dataclasses import dataclass


@dataclass(frozen=True)
class Configuration:
    """Конфигурация приложения."""

    pass


config = Configuration()
"""Единая конфигурация приложения."""
