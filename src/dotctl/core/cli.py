"""
Cli Interface - ArgumentParser Builder
"""

from pathlib import Path
import os
import argparse
from typing import Literal
from dataclasses import dataclass
from enum import Enum


@dataclass(frozen=True)
class ItemSelectionOp:
    action: Literal["include", "exclude"]
    items: tuple[str, ...]


def parse_items(value: str) -> tuple[str, ...]:
    return tuple(x.strip() for x in value.split(",") if x.strip())


ITEM_SELECTION = "item_selection_ops"


class ItemSelectionAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        ops = getattr(namespace, ITEM_SELECTION, None)

        if ops is None:
            ops = []
            setattr(namespace, ITEM_SELECTION, ops)

        action = {
            "--items": "include",
            "--exclude": "exclude",
        }[option_string]

        ops.append(
            ItemSelectionOp(
                action=action,
                items=parse_items(values),
            )
        )


PRESET_SELECTION = "preset_selection_ops"


class PresetSelectAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        ops = getattr(namespace, PRESET_SELECTION, None)
        if ops is None:
            ops = set()
            setattr(namespace, PRESET_SELECTION, ops)
        for p in parse_items(values):
            ops.add(p)


def default_config_dir() -> Path:
    xdg_dir = os.getenv("XDG_CONFIG_HOME")
    if xdg_dir:
        return Path(xdg_dir) / "dotctl"
    return Path.home() / ".config" / "dotctl"


class ColorMode(Enum):
    ALWAYS = "always"
    AUTO = "auto"
    NEVER = "never"


def parser_add_preset_attr(p: argparse.ArgumentParser):
    p.add_argument(
        "--preset",
        metavar="<preset>[,preset]",
        help="presets to add to action list",
    )


def parser_add_item_attr(p: argparse.ArgumentParser):
    p.add_argument(
        "--items",
        action=ItemSelectionAction,
        metavar="<item>[,<item>]",
        help="items to include in action list",
    )
    p.add_argument(
        "--exclude",
        action=ItemSelectionAction,
        metavar="<item>[,<item>]",
        help="items to exclude from action list",
    )


def build_argparser(bin: str) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog=bin,
        description="Yet another dotfiles manager powered by YAML and JINJA2",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            f"examples:\n"
            f"  {bin} init --items=mpd,rmpc\n"
            f"  {bin} install --items=alacritty,nvim,fish\n"
            f"  {bin} -n install --items=alacritty,nvim,fish\n"
            f"  {bin} -v install --items=alacritty,nvim,fish\n"
            f"  {bin} install --items=zsh,nvim,fish --exclude=zsh\n"
            f"  {bin} install --preset=linux-basic --exclude=zsh,bash\n"
            f"  {bin} install --preset=niri,linux-basic --items=keyd,lsd\n"
            f"  {bin} uninstall --items=zsh,bash\n"
            f"  {bin} explain dotctl item preset\n"
            f"  {bin} gen-completion fish\n"
        ),
    )

    # --------------------------------------------------------------------------
    # Global Options
    # --------------------------------------------------------------------------
    parser.add_argument(
        "-n",
        "--dry-run",
        action="store_true",
        help="Print the steps to execute",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Print the steps while executing",
    )
    parser.add_argument(
        "-C",
        "--config",
        metavar="DIR",
        type=Path,
        default=default_config_dir(),
        help="Global dotctl config dir",
    )
    parser.add_argument(
        "--color",
        type=ColorMode,
        metavar="COLOR_MODE",
        default=ColorMode.AUTO,
        help="Color display mode on output <always|auto|never>",
    )
    parser.add_argument(
        "--log-file",
        type=str,
        metavar="FILE",
        help="Assign log output file",
    )
    parser.add_argument(
        "--log-level",
        type=str,
        metavar="LOG_LEVEL",
        help="Set log level",
    )

    # --------------------------------------------------------------------------
    # Subcommands
    # --------------------------------------------------------------------------
    sub = parser.add_subparsers(dest="command", metavar="<command>")

    DESC_STR = "Initialize a dotfiles dir"
    p = sub.add_parser("init", help=DESC_STR, description=DESC_STR)

    DESC_STR = "Initialize an item by a template"
    p = sub.add_parser("new", help=DESC_STR, description=DESC_STR)
    parser_add_item_attr(p)
    parser_add_preset_attr(p)

    DESC_STR = "Install items"
    p = sub.add_parser("install", help=DESC_STR, description=DESC_STR)
    parser_add_item_attr(p)
    parser_add_preset_attr(p)

    DESC_STR = "Uninstall items"
    p = sub.add_parser("uninstall", help=DESC_STR, description=DESC_STR)
    parser_add_item_attr(p)
    parser_add_preset_attr(p)

    DESC_STR = "Print manual of topics"
    p = sub.add_parser("explain", help=DESC_STR, description=DESC_STR)
    p.add_argument(
        "--no-pager",
        action="store_true",
        help="Disable pager when printing help",
    )
    # TODO: Use 

    DESC_STR = "Generate shell completions"
    p = sub.add_parser("gen-completion", help=DESC_STR, description=DESC_STR)

    return parser
