"""Проверки команды python -m toolkit."""

import os
import subprocess
import sys
from pathlib import Path

import pytest

PROJECT_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_DIR / "src"


def run_toolkit(*args: str) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(SRC_DIR)
    return subprocess.run(
        [sys.executable, "-m", "toolkit", *args],
        cwd=PROJECT_DIR,
        env=env,
        capture_output=True,
        text=True,
        check=False,
        timeout=10,
    )


def test_help_exits_with_code_zero():
    completed = run_toolkit("--help")
    assert completed.returncode == 0
    assert "calc" in completed.stdout
    assert "convert" in completed.stdout
    assert completed.stderr == ""


def test_calc_command_prints_result():
    completed = run_toolkit("calc", "2+3*4")
    assert completed.returncode == 0
    assert completed.stdout.strip() == "14"
    assert completed.stderr == ""


def test_convert_command_prints_result():
    completed = run_toolkit("convert", "1000", "--from", "mm", "--to", "m")
    assert completed.returncode == 0
    assert completed.stdout.strip() == "1"
    assert completed.stderr == ""


def test_convert_accepts_uppercase_units():
    completed = run_toolkit("convert", "1.5", "--from", "KG", "--to", "G")
    assert completed.returncode == 0
    assert float(completed.stdout) == pytest.approx(1500)


def test_user_error_goes_to_stderr_with_code_2():
    completed = run_toolkit("calc", "1/0")
    assert completed.returncode == 2
    assert completed.stdout == ""
    assert "Деление на ноль" in completed.stderr


def test_incompatible_units_exit_with_code_2():
    completed = run_toolkit("convert", "1", "--from", "kg", "--to", "m")
    assert completed.returncode == 2
    assert completed.stdout == ""
    assert "Несовместимые" in completed.stderr


def test_negative_temperature_is_a_value_not_a_flag():
    completed = run_toolkit("convert", "-273.15", "--from", "c", "--to", "k")
    assert completed.returncode == 0
    assert float(completed.stdout) == pytest.approx(0.0, abs=1e-6)
