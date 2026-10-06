"""Командная строка пакета toolkit.

Пример запуска: python -m toolkit calc "2 + 3 * 4"
        python -m toolkit convert 1000 --from mm --to m
"""

import argparse
import sys

from toolkit.calculator import evaluate
from toolkit.converter import convert
from toolkit.errors import ToolkitError


def build_parser() -> argparse.ArgumentParser:
    """Описывает команды calc и convert."""
    parser = argparse.ArgumentParser(
        prog="python -m toolkit",
        description="Калькулятор и конвертер величин",
    )
    commands = parser.add_subparsers(dest="command", required=True)

    calc = commands.add_parser("calc", help="посчитать выражение")
    calc.add_argument("expression", help='например: "2 + 3 * 4"')

    convert_command = commands.add_parser("convert", help="перевести единицы")
    convert_command.add_argument("value", help="число")
    convert_command.add_argument(
        "--from",
        required=True,
        dest="source_unit",
        help="откуда: mm, cm, m, km, g, kg, c, f, k",
    )
    convert_command.add_argument(
        "--to",
        required=True,
        dest="target_unit",
        help="куда: единица из той же группы",
    )
    return parser


def format_result(value: int | float) -> str:
    """Показывает число без хвостовых нулей: 2.0 как 2, 2.5 как 2.5.
    Целое печатается целиком. Через float большое целое потеряло бы цифры.
    """
    if isinstance(value, int):
        return str(value)
    rounded = round(value, 10)
    if rounded == 0:
        return "0"
    return f"{rounded:.10f}".rstrip("0").rstrip(".")


def main(argv: list[str] | None = None) -> None:
    """Читает аргументы, вызывает ядро и печатает ответ или ошибку."""
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        if args.command == "calc":
            result = evaluate(args.expression)
        else:
            result = convert(args.value, args.source_unit, args.target_unit)
    except ToolkitError as error:
        print(error, file=sys.stderr)
        sys.exit(2)

    print(format_result(result))


if __name__ == "__main__":
    main()
