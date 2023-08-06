import sys

from rich.console import Console
from rich.table import Table

from .constants import DOT_CHAR

console = Console()
rich_print = console.print  # Rich variant
pyprint = print  # Python variant


def newline():
    print("\n", end="")


def print_both_sides(left, right):
    grid = Table.grid(expand=True)
    grid.add_column()
    grid.add_column(justify="right")
    grid.add_row(left, right)

    rich_print(grid)


def render_rich_text(text, highlight=False):
    with console.capture() as capture:
        rich_print(text, highlight=highlight)

    return capture.get()


def print_line(rule_style="dim green", char="─"):
    console.rule(style=rule_style, characters=char)


def observer_message(message, style="yellow"):
    return f"[{style}]observer[/{style}] [dim]{DOT_CHAR}[/dim] {message}"


def print_observer_error(message, style="red"):
    rich_print(
        f"[{style}]observer error[/{style}] [dim]{DOT_CHAR}[/dim] [red]{message}[/red]"
    )
    sys.exit(1)
