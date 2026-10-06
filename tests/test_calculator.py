"""Тесты калькулятора."""

from pathlib import Path

import pytest

from toolkit import evaluate
from toolkit.calculator import calculate, tokenize, validate
from toolkit.errors import CalculatorError

SRC = Path(__file__).resolve().parents[1] / "src" / "toolkit"


def test_multiplication_has_priority_over_addition():
    tokens = tokenize("2+3*4")
    validate(tokens)
    assert calculate(tokens) == 14
    assert evaluate("2+3*4") == 14


def test_division_of_integers_returns_fraction():
    assert evaluate("10 / 4") == 2.5


def test_unary_minus_after_multiplication():
    assert evaluate("2*-3") == -6
    assert evaluate("2 * -3") == -6


def test_plus_then_unary_minus():
    # 1+-2 — это 1 + (-2), не ошибка и не единица.
    assert evaluate("1+-2") == -1


def test_spaces_between_tokens_do_not_matter():
    assert evaluate("  10 / 4 + 2 ") == 4.5


def test_mixed_negative_numbers():
    assert evaluate("-5 + 2 * -3") == -11


def test_division_goes_left_to_right():
    assert evaluate("8/4/2") == 1


def test_tokenize_keeps_numbers_and_operators():
    assert tokenize("2 + 3.5 * -4") == [
        ("number", "2"),
        ("operator", "+"),
        ("number", "3.5"),
        ("operator", "*"),
        ("operator", "-"),
        ("number", "4"),
    ]


def test_huge_integers_keep_all_digits():
    # float хранит примерно 15 цифр, поэтому такое произведение надо считать в int.
    left = "10000000000000000000000000000000000000000"
    right = "10000000000000000000000000000000000"
    assert evaluate(f"{left}*{right}") == int(left) * int(right)


def test_empty_expression_is_rejected():
    with pytest.raises(CalculatorError, match="Пустое выражение"):
        evaluate("")
    with pytest.raises(CalculatorError, match="Пустое выражение"):
        evaluate("   ")


def test_invalid_character_is_rejected():
    with pytest.raises(CalculatorError, match="Недопустимый символ"):
        evaluate("2+a")


def test_two_operators_in_a_row_are_rejected():
    with pytest.raises(CalculatorError, match="Два оператора подряд"):
        evaluate("2*/3")


def test_missing_operand_is_rejected():
    with pytest.raises(CalculatorError, match="Пропущен операнд"):
        evaluate("2+")
    with pytest.raises(CalculatorError, match="Пропущен операнд"):
        evaluate("*2")


def test_division_by_zero_is_rejected():
    with pytest.raises(CalculatorError, match="Деление на ноль"):
        evaluate("1/0")
    with pytest.raises(CalculatorError, match="Деление на ноль"):
        evaluate("1 / 0")


def test_core_does_not_call_eval_input_or_print():
    for name in ("calculator.py", "converter.py"):
        source = (SRC / name).read_text(encoding="utf-8")
        assert "eval(" not in source
        assert "exec(" not in source
        assert "literal_eval" not in source
        assert "input(" not in source
        assert "print(" not in source
