__all__ = ["setup_logger"]

import sys
from typing import TYPE_CHECKING

from loguru import logger

if TYPE_CHECKING:
    from loguru import Logger


def setup_logger(
    name: str = "logs",
    base_dir: str = "logs",
    stdout_level: str = "DEBUG",
    file_level: str = "DEBUG",
    enqueue: bool = False,
) -> "Logger":
    """Настраивает логирование приложения через loguru.

    Args:
        name: Имя файла лога (без расширения), создаётся в директории base_dir.
        base_dir: Базовая директория для хранения файлов логов.
        stdout_level: Уровень логирования для вывода в консоль.
        file_level: Уровень логирования для записи в файл.
        enqueue: Включить асинхронное (thread-safe) логирование.

    Returns:
        Настроенный экземпляр loguru.Logger.

    """
    # Remove all existing logging handlers.
    logger.remove()

    # Console logging configuration.
    logger.add(
        sys.stderr,
        level=stdout_level,
        format="<white>{time: %d.%m %H:%M:%S}</white>|"
        "<level>{level}</level>|"
        "<bold>{message}</bold>",
    )

    # File logging configuration.
    logger.add(
        sink="/".join([p for p in [base_dir, f"{name}.log"] if p]),
        level=file_level,
        format="<white>{time: %d.%m %H:%M:%S.%f}</white> | "
        "<level>{level}</level>| "
        "|{name} {function} line:{line}| "
        "<bold>{message}</bold>",
        retention="30 days",  # Keep logs for 30 days.
        rotation="10 MB",  # Rotate logs when size exceeds 10 MB.
        compression="zip",  # Compress logs as .zip.
        encoding="utf-8",  # Log file encoding.
        enqueue=enqueue,  # Async logging mode.
    )

    return logger
