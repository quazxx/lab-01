"""Конвертер длины, массы и температуры.

Результат всегда float. Разные группы единиц между собой не переводятся.
"""

import math

from toolkit.constants import (
    ABSOLUTE_ZERO_C,
    ABSOLUTE_ZERO_TOLERANCE,
    KELVIN_OFFSET,
    LENGTH_IN_METERS,
    MASS_IN_GRAMS,
    TEMPERATURE_UNITS,
)
from toolkit.errors import ConverterError


def convert(value_text: str, source_unit: str, target_unit: str) -> float:
    """Переводит число из одной единицы в другую."""
    value = _parse_value(value_text)
    source = source_unit.strip().lower()
    target = target_unit.strip().lower()

    source_group = _group(source)
    target_group = _group(target)
    if source_group != target_group:
        raise ConverterError(f"Несовместимые единицы: {source} и {target}")

    if source_group == "length":
        return value * LENGTH_IN_METERS[source] / LENGTH_IN_METERS[target]
    if source_group == "mass":
        return value * MASS_IN_GRAMS[source] / MASS_IN_GRAMS[target]
    return _convert_temperature(value, source, target)


def _parse_value(value_text: str) -> float:
    """Превращает текст команды в конечное число."""
    try:
        value = float(value_text.strip())
    except ValueError:
        raise ConverterError(f"Неверное числовое значение: {value_text}") from None
    if not math.isfinite(value):
        raise ConverterError(f"Неверное числовое значение: {value_text}")
    return value


def _group(unit: str) -> str:
    """Возвращает группу единицы: length, mass или temperature."""
    if unit in LENGTH_IN_METERS:
        return "length"
    if unit in MASS_IN_GRAMS:
        return "mass"
    if unit in TEMPERATURE_UNITS:
        return "temperature"
    raise ConverterError(f"Неизвестная единица: {unit}")


def _convert_temperature(value: float, source: str, target: str) -> float:
    """Переводит температуру через градусы Цельсия.

    Формулы: F = C * 9/5 + 32, K = C + 273.15.
    Ниже абсолютного нуля переводить нельзя.
    """
    celsius = _to_celsius(value, source)
    if celsius < ABSOLUTE_ZERO_C - ABSOLUTE_ZERO_TOLERANCE:
        raise ConverterError("Температура ниже абсолютного нуля")
    return _from_celsius(celsius, target)


def _to_celsius(value: float, unit: str) -> float:
    """Приводит температуру к градусам Цельсия."""
    if unit == "c":
        return value
    if unit == "k":
        return value - KELVIN_OFFSET
    return (value - 32.0) * 5.0 / 9.0


def _from_celsius(celsius: float, unit: str) -> float:
    """Переводит градусы Цельсия в нужную единицу."""
    if unit == "c":
        return celsius
    if unit == "k":
        return celsius + KELVIN_OFFSET
    return celsius * 9.0 / 5.0 + 32.0
