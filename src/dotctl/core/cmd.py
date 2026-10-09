import argparse


class PipeLineError(Exception):
    def __init__(self, msg):
        super().__init__(msg)


def cmd_install(ctx: argparse.Namespace):
    raise PipeLineError(f"Command `{ctx.command}` not implemented")


def cmd_uninstall(ctx: argparse.Namespace):
    raise PipeLineError(f"Command `{ctx.command}` not implemented")


def cmd_new(ctx: argparse.Namespace):
    raise PipeLineError(f"Command `{ctx.command}` not implemented")


def cmd_init(ctx: argparse.Namespace):
    raise PipeLineError(f"Command `{ctx.command}` not implemented")


def cmd_explain(ctx: argparse.Namespace):
    raise PipeLineError(f"Command `{ctx.command}` not implemented")


def cmd_gen_completion(ctx: argparse.Namespace):
    raise PipeLineError(f"Command `{ctx.command}` not implemented")
