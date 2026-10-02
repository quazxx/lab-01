"""Константы для калькулятора и конвертера."""

NUMBER = "number"
OPERATOR = "operator"

BINARY_OPERATORS = "+-*/"
UNARY_SIGNS = "+-"


""" Сколько метров в одной единице."""
LENGTH_IN_METERS = {
    "mm": 0.001,
    "cm": 0.01,
    "m": 1.0,
    "km": 1000.0,
}


"""Сколько граммов в одной единице."""
MASS_IN_GRAMS = {
    "g": 1.0,
    "kg": 1000.0,
}


"""Единицы измерения температуры."""
TEMPERATURE_UNITS = ("c", "f", "k")

# 0 °C = 273.15 K, абсолютный ноль = −273.15 °C = 0 K.
KELVIN_OFFSET = 273.15
ABSOLUTE_ZERO_C = -273.15
ABSOLUTE_ZERO_TOLERANCE = 1e-6
