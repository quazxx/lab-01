"""Тесты конвертера."""

import pytest

from toolkit import convert
from toolkit.errors import ConverterError


def test_millimeters_to_meters():
    assert convert("1000", "mm", "m") == 1


def test_centimeters_to_meters():
    assert convert("100", "cm", "m") == 1


def test_kilograms_to_grams():
    assert convert("1.5", "kg", "g") == 1500


def test_grams_to_kilograms():
    assert convert("500", "g", "kg") == 0.5


def test_zero_celsius_to_fahrenheit():
    assert convert("0", "c", "f") == 32


def test_absolute_zero_celsius_to_kelvin():
    assert convert("-273.15", "c", "k") == pytest.approx(0.0, abs=1e-6)


def test_kelvin_freezing_point_to_celsius():
    assert convert("273.15", "k", "c") == pytest.approx(0.0, abs=1e-6)


def test_temperature_below_absolute_zero():
    with pytest.raises(ConverterError, match="Температура ниже абсолютного нуля"):
        convert("-273.16", "C", "K")
    with pytest.raises(ConverterError, match="Температура ниже абсолютного нуля"):
        convert("-460", "f", "c")


def test_incompatible_units():
    with pytest.raises(ConverterError, match="Несовместимые единицы"):
        convert("1", "kg", "m")


def test_unknown_unit():
    with pytest.raises(ConverterError, match="Неизвестная единица"):
        convert("1", "lb", "kg")


def test_units_ignore_case():
    assert convert("1000", "MM", "M") == 1
    assert convert("0", "C", "F") == 32


def test_invalid_number():
    with pytest.raises(ConverterError, match="Неверное числовое значение"):
        convert("abc", "m", "cm")
