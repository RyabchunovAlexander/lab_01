import os
import subprocess
import sys

import pytest

from toolkit.calculator import calculate
from toolkit.converter import convert
from toolkit.errors import ToolkitError

# Настройка путей для корректного поиска пакета toolkit
CLI_ENV = os.environ.copy()
CLI_ENV["PYTHONPATH"] = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../src")
)


def test_calc_mandatory_addition_and_multiplication() -> None:
    """Проверка приоритета операций из чек-листа."""
    assert calculate("2+3*4") == 14.0


def test_calc_mandatory_division() -> None:
    """Проверка вещественного деления из чек-листа."""
    assert calculate("10 / 4") == 2.5


def test_calc_mandatory_unary_multiplication() -> None:
    """Проверка умножения отрицательных чисел из чек-листа."""
    assert calculate("-2 * -3") == 6.0


def test_calc_mandatory_unary_addition() -> None:
    """Проверка сложения с унарным минусом из чек-листа."""
    assert calculate("1+-2") == -1.0


def test_calc_extra_subtraction() -> None:
    """Дополнительная проверка базового вычитания."""
    assert calculate("100 - 45") == 55.0


def test_calc_extra_basic_division() -> None:
    """Дополнительная проверка деления нацело в float."""
    assert calculate("25 / 5") == 5.0


def test_convert_length_mm_to_m() -> None:
    """Конвертация миллиметры в метры."""
    assert convert("1000", "mm", "m") == 1.0


def test_convert_length_km_to_m() -> None:
    """Конвертация километры в метры."""
    assert convert("2.5", "km", "m") == 2500.0


def test_convert_mass_kg_to_g() -> None:
    """Конвертация килограммы в граммы."""
    assert convert("1.5", "kg", "g") == 1500.0


def test_convert_mass_g_to_kg() -> None:
    """Конвертация граммы в килограммы."""
    assert convert("100", "g", "kg") == 0.1


def test_convert_temp_c_to_f() -> None:
    """Конвертация Цельсий в Фаренгейт."""
    assert convert("0", "c", "f") == 32.0


def test_convert_temp_c_to_k() -> None:
    """Конвертация: Абсолютный ноль в Кельвины."""
    assert convert("-273.15", "c", "k") == pytest.approx(0.0)


def test_convert_case_invariant_mass() -> None:
    """Проверка инвариантности к верхнему регистру."""
    assert convert("1.5", "KG", "G") == 1500.0


def test_convert_case_invariant_length() -> None:
    """Проверка инвариантности к верхнему регистру."""
    assert convert("100", "M", "CM") == 10000.0


def test_calc_empty_string() -> None:
    """Негативный тест: пустая строка в калькуляторе."""
    with pytest.raises(ToolkitError, match="пустое выражение"):
        calculate("   ")


def test_calc_two_operators() -> None:
    """Негативный тест: два бинарных оператора подряд."""
    with pytest.raises(ToolkitError, match="два бинарных оператора подряд"):
        calculate("2*/3")


def test_calc_invalid_char() -> None:
    """Негативный тест: недопустимый символ в калькуляторе."""
    with pytest.raises(ToolkitError, match="недопустимый символ"):
        calculate("2+a")


def test_calc_division_by_zero() -> None:
    """Негативный тест: деление на ноль."""
    with pytest.raises(ToolkitError, match="деление на ноль"):
        calculate("10 / 0")


def test_convert_below_absolute_zero() -> None:
    """Негативный тест: температура ниже абсолютного нуля."""
    with pytest.raises(ToolkitError, match="температура ниже абсолютного нуля"):
        convert("-300", "c", "k")


def test_convert_incompatible_groups() -> None:
    """Негативный тест: несовместимые группы единиц."""
    with pytest.raises(ToolkitError, match="несовместимые единицы"):
        convert("100", "kg", "m")


def test_convert_unknown_unit() -> None:
    """Негативный тест: абсолютно неизвестная единица измерения."""
    with pytest.raises(ToolkitError, match="неизвестн"):
        convert("50", "abc", "m")


def test_cli_help_success() -> None:
    """CLI тест: команда --help завершается с кодом 0."""
    result = subprocess.run(
        [sys.executable, "-m", "toolkit", "--help"],
        capture_output=True,
        text=True,
        check=False,
        env={"PYTHONPATH": "src"},
    )
    assert result.returncode == 0
    assert "calc" in result.stdout or "calculator" in result.stdout.lower()


def test_cli_error_code_two() -> None:
    """CLI тест: пользовательская ошибка ядра даёт системный код 2."""
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "toolkit",
            "convert",
            "100",
            "--from",
            "kg",
            "--to",
            "m",
        ],
        capture_output=True,
        text=True,
        check=False,
        env={"PYTHONPATH": "src"},
    )
    assert result.returncode == 2
    assert "Ошибка: несовместимые единицы" in result.stderr


def test_cli_missing_command_error() -> None:
    """CLI тест: вызов утилиты вообще без указания команды даёт код 2."""
    result = subprocess.run(
        [sys.executable, "-m", "toolkit"],
        capture_output=True,
        text=True,
        check=False,
        env={"PYTHONPATH": "src"},
    )
    assert result.returncode == 2

