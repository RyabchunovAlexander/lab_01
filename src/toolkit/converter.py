from toolkit.errors import ToolkitError

# Базовая матрица коэффициентов перевода к эталону (эталон длины - m, массы - g)
FACTORS = {
    "length": {"mm": 0.001, "cm": 0.01, "m": 1.0, "km": 1000.0},
    "mass": {"g": 1.0, "kg": 1000.0},
}


def get_unit_group(unit: str) -> str:
    """Определяет физическую группу, к которой относится единица измерения."""
    if unit in FACTORS["length"]:
        return "length"
    if unit in FACTORS["mass"]:
        return "mass"
    if unit in ("c", "f", "k"):
        return "temperature"
    # Ошибка: неизвестная единица измерения
    raise ToolkitError(f"Unknown unit: '{unit}'")


def to_kelvin(value: float, unit: str) -> float:
    """Вспомогательная функция для перевода любой шкалы в Кельвины.

    Нужна строго для проверки ограничения абсолютного нуля.
    """
    if unit == "k":
        return value
    if unit == "c":
        return value + 273.15
    if unit == "f":
        return (value - 32) * 5 / 9 + 273.15
    return 0.0


def convert_temperature(value: float, from_unit: str, to_unit: str) -> float:
    """Выполняет конвертацию между температурными шкалами (C, F, K)."""
    # 1. Сначала приводим исходную шкалу к базовому Цельсию
    if from_unit == "c":
        celsius = value
    elif from_unit == "k":
        celsius = value - 273.15
    else:  # f
        celsius = (value - 32) * 5 / 9

    # 2. Из Цельсия переводим в целевую шкалу
    if to_unit == "c":
        return celsius
    elif to_unit == "k":
        return celsius + 273.15
    else:  # f
        return celsius * 9 / 5 + 32


def convert(value_str: str, from_unit: str, to_unit: str) -> float:
    """Главная функция вычислительного ядра конвертера.

    Принимает строку-значение и две единицы измерения. Возвращает float.
    """
    # 1. Валидация: проверяем, что введено корректное число
    try:
        value = float(value_str)
    except ValueError:
        raise ToolkitError("Invalid numeric value")

    # 2. Приводим строки к нижнему регистру согласно правилу инвариантности к регистру
    from_unit = from_unit.lower()
    to_unit = to_unit.lower()

    # 3. Определяем группы единиц
    group_from = get_unit_group(from_unit)
    group_to = get_unit_group(to_unit)

    # 4. Валидация: запрещаем перевод между несовместимыми группами (например, kg в m)
    if group_from != group_to:
        raise ToolkitError(
            f"Incompatible units: cannot convert {group_from} to {group_to}"
        )

    # 5. Вычисление
    if group_from == "temperature":
        # Проверка обязательного ограничения: температура ниже абсолютного нуля запрещена
        if to_kelvin(value, from_unit) < 0:
            raise ToolkitError("Temperature below absolute zero is forbidden")
        return float(convert_temperature(value, from_unit, to_unit))
    else:
        # Для длины и массы делаем перевод через эталон (инвариант)
        factor_from = FACTORS[group_from][from_unit]
        factor_to = FACTORS[group_from][to_unit]

        # Переводим в эталон (умножением), а затем из эталона в целевую (делением)
        base_value = value * factor_from
        return float(base_value / factor_to)
