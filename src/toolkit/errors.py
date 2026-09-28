import sys


class ToolkitError(Exception):
    """Базовое исключение для нашего пакета toolkit."""


def handle_error(message: str) -> None:
    """Выводит сообщение об ошибке в stderr и завершает процесс с кодом 2."""


    print(f"Ошибка: {message}", file=sys.stderr)
    sys.exit(2)
