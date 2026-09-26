import argparse

from toolkit.calculator import calculate
from toolkit.converter import convert
from toolkit.errors import ToolkitError, handle_error


def main() -> None:
    """Точка входа CLI интерфейса пакета toolkit.

    Разбирает аргументы командной строки, вызывает соответствующие ядра
    вычислений и централизованно обрабатывает возникающие ошибки.
    """
    # Создаем главный парсер аргументов командной строки
    parser = argparse.ArgumentParser(
        prog="python -m toolkit",
        description="Toolkit CLI Utilities: калькулятор выражений и конвертер величин.",
    )

    # Добавляем подпарсеры для разделения команд 'calc' и 'convert'
    # dest="command" запишет имя вызванной команды (calc или convert) в переменную
    commands = parser.add_subparsers(dest="command", required=True)

    # --- Настройка команды 'calc' ---
    calc_parser = commands.add_parser("calc", help="Вычислить математическое выражение")
    # Добавляем обязательный позиционный аргумент для строки выражения
    calc_parser.add_argument("expression", help="Математическое выражение в кавычках")

    # --- Настройка команды 'convert' ---
    convert_parser = commands.add_parser("convert", help="Конвертировать величины")
    # Добавляем позиционный аргумент для значения (передается как строка для ядра)
    convert_parser.add_argument("value", help="Числовое значение для конвертации")
    # Добавляем обязательный именованный флаг --from
    convert_parser.add_argument(
        "--from", dest="from_unit", required=True, help="Исходная единица измерения"
    )
    # Добавляем обязательный именованный флаг --to
    convert_parser.add_argument(
        "--to", dest="to_unit", required=True, help="Целевая единица измерения"
    )

    # Запускаем разбор аргументов, переданных из терминала
    args = parser.parse_args()

    try:
        # Маршрутизация: смотрим, какая команда была вызвана пользователем
        if args.command == "calc":
            # Передаем строку выражения в ядро калькулятора
            result = calculate(args.expression)
            # Выводим успешный результат в стандартный stdout
            print(result)

        elif args.command == "convert":
            # Передаем параметры в ядро конвертера величин
            result = convert(args.value, args.from_unit, args.to_unit)
            # Выводим успешный результат в стандартный stdout
            print(result)

    except ToolkitError as e:
        # Если ядро выбросило наше контролируемое исключение — передаем его текст
        # в обработчик ошибок, который выведет его в stderr и вернет код 2.
        handle_error(str(e))


if __name__ == "__main__":
    main()
