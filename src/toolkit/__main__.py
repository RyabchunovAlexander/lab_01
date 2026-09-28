import argparse

from toolkit.calculator import calculate
from toolkit.converter import convert
from toolkit.errors import ToolkitError, handle_error


def main() -> None:
    """Точка входа CLI интерфейса пакета toolkit.

    Разбирает аргументы командной строки, вызывает соответствующие ядра
    вычислений и централизованно обрабатывает возникающие ошибки.
    """
    # Настраиваем главный парсер командной строки
    parser = argparse.ArgumentParser(
        prog="python -m toolkit",
        description="Toolkit CLI Utilities: калькулятор выражений и конвертер величин.",
    )

    # Создаем блок для команд 'calc' и 'convert'
    commands = parser.add_subparsers(dest="command", required=True)

    # Настройка команды 'calc'
    calc_parser = commands.add_parser("calc", help="Вычислить математическое выражение")
    calc_parser.add_argument("expression", help="Математическое выражение в кавычках")

    # Настройка команды 'convert'
    convert_parser = commands.add_parser("convert", help="Конвертировать величины")
    convert_parser.add_argument("value", help="Числовое значение для конвертации")
    convert_parser.add_argument(
        "--from", dest="from_unit", required=True, help="Исходная единица измерения"
    )
    convert_parser.add_argument(
        "--to", dest="to_unit", required=True, help="Целевая единица измерения"
    )

    # Считываем аргументы из терминала
    args = parser.parse_args()

    try:
        # Проверяем, что ввел пользователь
        if args.command == "calc":
            result = calculate(args.expression)
            print(result)

        elif args.command == "convert":
            result = convert(args.value, args.from_unit, args.to_unit)
            print(result)

    except ToolkitError as e:
        # Отправляем ошибку в stderr и выходим с кодом 2
        handle_error(str(e))


if __name__ == "__main__":
    main()
