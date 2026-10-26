#!/usr/bin/python3

import argparse
import subprocess

import utils

_BASE_ROM_PATH = "/home/pi/RetroPie/roms"

def _get_rom_path(args):
    for a in args:
        if a.startswith(_BASE_ROM_PATH):
            return a
    raise RuntimeError("Failed to find rom")


_XDELTA_PATCHER_SYSTEMS = [
    "dreamcast",
    "psp",
    "psx",
    "segacd",
]


def _should_do_xdelta(args):
    if args.xdelta_patcher == "force":
        return True
    if args.xdelta_patcher == "auto":
        config_path = utils.get_ra_config_path(args.args)
        system = utils.get_ra_system_from_path(config_path)
        if system in _XDELTA_PATCHER_SYSTEMS:
            return True
    return False


_DEFAULT_SCRIPT_CHOICE = "auto"

_SCRIPT_ENABLE_CHOICES = (
    _DEFAULT_SCRIPT_CHOICE,
    "force",
    "disable",
)


def _main():
    parser = argparse.ArgumentParser(
        prog="retroarch-orchestrator",
        description="Run retroarch with optional steps/configuration automtically applied",
    )
    parser.add_argument(
        "--savepath-injector",
        choices=_SCRIPT_ENABLE_CHOICES,
        default=_DEFAULT_SCRIPT_CHOICE,
        help="Control savepath-injector execution flow (default: %(default)s)",
    )
    parser.add_argument(
        "--xdelta-patcher",
        choices=_SCRIPT_ENABLE_CHOICES,
        default=_DEFAULT_SCRIPT_CHOICE,
        help="Control xdelta-patcher execution flow (default: %(default)s)",
    )
    parser.add_argument(
        "--savepath-injector-arg",
        action="append",
        default=[],
        help="Extra arguments to pass to savepath-injector script",
    )
    parser.add_argument(
        "--xdelta-patcher-arg",
        action="append",
        default=[],
        help="Extra arguments to pass to xdelta-patcher script",
    )
    parser.add_argument(
        "args",
        nargs="*",
    )

    args = parser.parse_args()
    final_command = []
    if args.savepath_injector != "disable":
        final_command.extend(
            ["savepath-injector.py", *args.savepath_injector_arg, "--"]
        )

    if _should_do_xdelta(args):
        # the rom probably won't be the last argument, so figure it out and pass it explicitly'
        rom = _get_rom_path(args.args)
        final_command.extend(
            ["xdelta-patcher.py", "-f", rom, *args.xdelta_patcher_arg, "--"]
        )
    # add actual command
    final_command.extend(args.args)
    # print(f"{final_command}")
    subprocess.run(final_command, check=True)


if __name__ == "__main__":
    _main()
