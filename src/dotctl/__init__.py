"""dotctl - Yet another dotfiles manager powered by YAML and JINJA2

Python replacement for old `bootstrap` script.
"""

from dotctl.core.cmd import (
    PipeLineError,
    cmd_install,
    cmd_uninstall,
    cmd_init,
    cmd_new,
    cmd_explain,
    cmd_gen_completion,
)
import sys
import argparse
from dotctl.core.cli import build_argparser

HANDLERS = {
    "install": cmd_install,
    "uninstall": cmd_uninstall,
    "init": cmd_init,
    "new": cmd_new,
    "explain": cmd_explain,
    "gen-completion": cmd_gen_completion,
}


def run(ctx: argparse.Namespace) -> int:
    # init log
    assert(ctx.command)
    match ctx.command:
        case "install":
            return cmd_install(ctx)
        case _:
            # log unknown command
            print(f"Unknown command `{ctx.command=}`")
            return 1


def main(argv: list[str] | None = None) -> int:
    parser = build_argparser(sys.argv[0])
    ctx = parser.parse_args(argv)
    if not ctx.command:
        parser.print_help()
        return 0
    try:
        return run(ctx)
    except PipeLineError as err:
        print(f"{err=}")
        return 1
