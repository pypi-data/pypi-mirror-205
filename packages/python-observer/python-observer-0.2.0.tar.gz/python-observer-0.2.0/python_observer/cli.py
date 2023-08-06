import argparse

from .constants import DOT_CHAR
from .date import format_time, get_current_time, get_monotonic_time
from .display import newline, observer_message, print_both_sides, print_line
from .display import rich_print as print
from .misc import file_exists, get_python_version
from .watch import watch_file


def main():
    # sourcery skip: extract-method
    parser = argparse.ArgumentParser()

    parser.add_argument("script", help="the file to watch", type=str)
    parser.add_argument(
        "script_args",
        nargs=argparse.REMAINDER,
        help="additional arguments for the above file",
    )

    args = parser.parse_args()

    if not args.script:
        parser.print_help()

    try:
        command = [args.script] + args.script_args

        if file_exists(args.script):
            file_path = args.script
        else:
            print(
                observer_message(
                    f"[red]Error: File {args.script} does not exist", style="red"
                ),
                highlight=False,
            )
            exit()

        newline()

        print_both_sides(
            left=observer_message("[magenta]A file system watcher for Python files[/]"),
            right=f"[green]{get_current_time(time_format='%Y-%m-%d %I:%M:%S %p')} :watch:",
        )

        print_both_sides(
            left=observer_message(
                f"[green]watching file [blue]{file_path}[/blue] [dim]{DOT_CHAR}[/dim] [red]hit Ctrl + C to exit[/]"
            ),
            right=f"[blue]{get_python_version()}[/blue] :snake:",
        )

        newline()
        print_line(rule_style="cyan", char="━")
        newline()

        session_start_time = get_monotonic_time(as_seconds=True, should_round=False)

        watch_file(command, file_path=args.script)
    except KeyboardInterrupt:
        session_end_time = get_monotonic_time(as_seconds=True, should_round=False)
        newline()
        print(
            observer_message(
                f"[cyan]watch session took [yellow]{format_time(session_end_time - session_start_time)}"
            )
        )
        newline()
        print(observer_message(":wave: [red]Goodbye![/]"))
        newline()
        exit()


if __name__ == "__main__":
    main()
