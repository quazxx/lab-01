"""Калькулятор."""

from toolkit.constants import BINARY_OPERATORS, NUMBER, OPERATOR, UNARY_SIGNS
from toolkit.errors import CalculatorError

Token = tuple[str, str]
Number = int | float


def tokenize(expression: str) -> list[Token]:
    """Деление строки на числа и операторы. Пропуск пробелов."""
    tokens: list[Token] = []
    index = 0
    while index < len(expression):
        char = expression[index]
        if char.isspace():
            index += 1
            continue
        if char.isdigit() or char == ".":
            number, index = _read_number(expression, index)
            tokens.append((NUMBER, number))
            continue
        if char in BINARY_OPERATORS:
            tokens.append((OPERATOR, char))
            index += 1
            continue
        raise CalculatorError(f"Недопустимый символ: {char}")
    return tokens


def validate(tokens: list[Token]) -> None:
    """Проверяет, что токены складываются в нормальное выражение."""
    if not tokens:
        raise CalculatorError("Пустое выражение")

    expect_number = True
    previous_is_operator = False

    for kind, value in tokens:
        if expect_number:
            if kind == NUMBER:
                expect_number = False
                previous_is_operator = False
                continue
            # Плюс или минус перед числом - это знак, а не бинарная операция.
            if value in UNARY_SIGNS:
                previous_is_operator = True
                continue
            if previous_is_operator:
                raise CalculatorError("Два оператора подряд")
            raise CalculatorError("Пропущен операнд")

        if kind != OPERATOR:
            raise CalculatorError("Пропущен оператор")
        expect_number = True
        previous_is_operator = True

    if expect_number:
        raise CalculatorError("Пропущен операнд")


def calculate(tokens: list[Token]) -> Number:
    """Считает уже проверенные токены.

    Сначала умножение и деление, потом сложение и вычитание.
    Одинаковые операции идут слева направо."""
    numbers, operators = _apply_unary(tokens)
    numbers, operators = _collapse_high_priority(numbers, operators)

    result = numbers[0]
    for index, operator in enumerate(operators):
        result = _apply(result, operator, numbers[index + 1])
    return result


def evaluate(expression: str) -> Number:
    """Считает выражение целиком: разбор, проверка, вычисление."""
    tokens = tokenize(expression)
    validate(tokens)
    return calculate(tokens)


def _read_number(expression: str, index: int) -> tuple[str, int]:
    """Читает целое или дробное число, начиная с позиции index."""
    start = index
    has_dot = False
    has_digit = False

    while index < len(expression):
        char = expression[index]
        if char.isdigit():
            has_digit = True
            index += 1
            continue
        if char == "." and not has_dot:
            has_dot = True
            index += 1
            continue
        break

    if not has_digit:
        raise CalculatorError(f"Недопустимый символ: {expression[start]}")
    return expression[start:index], index


def _apply_unary(tokens: list[Token]) -> tuple[list[Number], list[str]]:
    """Приклеивает унарные плюс и минус к числу.

        Пример: 2 * -3 становится числами [2, -3] и оператором ['*'].
    Целое остаётся int, число с точкой становится float.
    """
    numbers: list[Number] = []
    operators: list[str] = []
    index = 0
    expect_number = True

    while index < len(tokens):
        kind, value = tokens[index]
        if not expect_number:
            operators.append(value)
            expect_number = True
            index += 1
            continue

        sign = 1
        while kind == OPERATOR:
            if value == "-":
                sign = -sign
            index += 1
            if index >= len(tokens):
                raise CalculatorError("Пропущен операнд")
            kind, value = tokens[index]

        number: Number = float(value) if "." in value else int(value)
        numbers.append(sign * number)
        expect_number = False
        index += 1

    if expect_number or not numbers:
        raise CalculatorError("Пропущен операнд")
    return numbers, operators


def _collapse_high_priority(
    numbers: list[Number],
    operators: list[str],
) -> tuple[list[Number], list[str]]:
    """Сворачивает * и /. Плюс и минус оставляет на второй проход."""
    collapsed_numbers = [numbers[0]]
    collapsed_operators: list[str] = []

    for index, operator in enumerate(operators):
        right = numbers[index + 1]
        if operator in ("*", "/"):
            collapsed_numbers[-1] = _apply(collapsed_numbers[-1], operator, right)
            continue
        collapsed_operators.append(operator)
        collapsed_numbers.append(right)

    return collapsed_numbers, collapsed_operators


def _apply(left: Number, operator: str, right: Number) -> float:
    """Применяет один оператор к двум уже известным числам."""
    if operator == "+":
        return left + right
    if operator == "-":
        return left - right
    if operator == "*":
        return left * right
    if right == 0:
        raise CalculatorError("Деление на ноль")
    return left / right
