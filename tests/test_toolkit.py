import pytest

from toolkit.calculator import calculate
from toolkit.converter import convert
from toolkit.errors import ToolkitError


# --- 1. ПОЗИТИВНЫЕ ТЕСТЫ КАЛЬКУЛЯТОРА (6 кейсов) ---
@pytest.mark.parametrize(
    "expression, expected",
    [
        ("2+3*4", 14),             # Обязательная проверка преподавателя
        ("10 / 4", 2.5),           # Обязательная проверка преподавателя
        ("-2 * -3", 6),            # Проверка унарных знаков
        ("1+-2", -1),              # Стык бинарного и унарного операторов
        ("  10.5  +  4.5  ", 15),  # Игнорирование пробелов и вещественные числа
        ("-5", -5),                # Выражение из одного отрицательного числа
    ],
)
def test_calculator_positive(expression, expected):
    """Тестирует корректный подсчет математических выражений ядра."""
    assert calculate(expression) == expected


# --- 2. НЕГАТИВНЫЕ ТЕСТЫ КАЛЬКУЛЯТОРА (5 обязательных кейсов) ---
@pytest.mark.parametrize(
    "invalid_expression",
    [
        "",       # Пустая строка
        "2*/3",   # Два бинарных оператора подряд
        "2+a",    # Недопустимый символ (буква)
        "1/0",    # Деление на ноль
        "5+",     # Пропущенный операнд на конце выражений
    ],
)
def test_calculator_negative(invalid_expression):
    """Тестирует, что ядро правильно выбрасывает исключения на плохой ввод."""
    with pytest.raises(ToolkitError):
        calculate(invalid_expression)


# --- 3. ТЕСТЫ КОНВЕРТЕРА ВЕЛИЧИН (4 кейса) ---
@pytest.mark.parametrize(
    "value, from_unit, to_unit, expected",
    [
        ("1000", "mm", "m", 1.0),
        ("1.5", "kg", "g", 1500.0),
        ("0", "c", "f", 32.0),
        ("100", "KM", "m", 100000.0),  # Проверка независимости от регистра
    ],
)
def test_converter_positive(value, from_unit, to_unit, expected):
    """Тестирует успешную конвертацию длин, масс и температур."""
    assert convert(value, from_unit, to_unit) == expected


def test_converter_absolute_zero_and_incompatible():
    """Тестирует граничные условия конвертера и несовместимость групп."""
    # Около абсолютного нуля с небольшой погрешностью float
    assert abs(convert("-273.15", "c", "k") - 0.0) < 1e-5

    # Ниже абсолютного нуля — должна быть ошибка
    with pytest.raises(ToolkitError):
        convert("-275", "c", "k")

    # Попытка перевести массу в длину — должна быть ошибка
    with pytest.raises(ToolkitError):
        convert("100", "kg", "m")


# --- 4. ИЗОЛИРОВАННЫЕ ТЕСТЫ CLI И ОШИБОК (2 кейса) ---
def test_cli_error_handling(capsys):
    """Тестирует, что утилита выводит ошибку в stderr и выдает код завершения 2."""
    from toolkit.errors import handle_error

    # Перехватываем системный выход sys.exit(2)
    with pytest.raises(SystemExit) as exc_info:
        handle_error("Test Error Message")

    # Проверяем, что код возврата равен 2
    assert exc_info.value.code == 2

    # Перехватываем вывод терминала и проверяем поток stderr
    captured = capsys.readouterr()
    assert "Error: Test Error Message" in captured.err
