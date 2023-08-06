import argparse
from inspect import cleandoc

from pyboxen import boxen

from .constants import DOT_CHAR
from .date import format_time, get_current_time, get_monotonic_time
from .display import (
    newline,
    observer_message,
    print_both_sides,
    print_line,
    pyprint,
    render_rich_text,
)
from .display import rich_print as print
from .misc import check_for_errors, get_observer_version, get_python_version
from .watch import watch_file


def main():
    class ObserverArgumentParser(argparse.ArgumentParser):
        def print_help(self):
            description = ":sparkles: Live reload for Python apps"

            pyprint(
                boxen(
                    cleandoc(
                        f"""
                        [bold][dim]{description}[/dim][/bold]

                        [bold][yellow]USAGE[/yellow][/bold]

                            [blue]observer[/blue] [magenta]\[file][/magenta]

                        [bold][yellow]ARGS[/yellow][/bold]

                            [magenta]file[/magenta]            The source file to watch
                                            [dim]Defaults to [blue]main.py[/blue] if not specified[/dim]
                                            [dim]Optional arguments for the file can be[/dim]
                                            [dim]appended at the end of the file name[/dim]

                        [bold][yellow]OPTIONS[/yellow][/bold]

                            [green]-h, --help[/green]      Show this help message
                            [green]-v, --version[/green]   Show version information

                        [bold][yellow]SOURCE CODE[/yellow][/bold]

                            🔗 [blue]https://github.com/savioxavier/observer[/blue]

                        [bold][yellow]DONATE[/yellow][/bold]

                            💖 [red]https://www.buymeacoffee.com/savioxavier[/red]
                        """
                    ),
                    style="rounded",
                    padding=1,
                    margin=1,
                    title="[bold][green]:eyes: observer[/green]",
                    title_alignment="center",
                    color="cyan",
                )
            )

    parser = ObserverArgumentParser()

    parser.add_argument(
        "script",
        help="the file to watch",
        nargs=argparse.OPTIONAL,
        type=str,
        default="main.py",
    )
    parser.add_argument(
        "script_args",
        nargs=argparse.REMAINDER,
        help="additional arguments for the above file",
    )
    parser.add_argument(
        "-v",
        "--version",
        help="Get current version",
        action="version",
        version=render_rich_text(
            f"[green]observer version[/green] [yellow]v{get_observer_version()}[/yellow]"
        ),
    )

    args = parser.parse_args()

    if not args.script:
        parser.print_help()

    try:
        command = [args.script] + args.script_args

        check_for_errors(args.script)

        # check_for_errors automatically exits if a file-related error occurs
        # If above check_for_errors yields nothing, then we're good to go
        # and we can assign file path as args.script

        file_path = args.script

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
