#!/usr/bin/python3

import argparse
import subprocess

import utils


def _get_rom_path(args):
    in_flag = False
    for a in args:
        if a[0] == "-":
            in_flag = True
            continue
        if in_flag:
            in_flag = False
            continue
        return a
    raise RuntimeError("Failed to find rom")


_XDELTA_PATCHER_SYSTEMS = [
    "dreamcast",
    "psp",
    "psx",
    "segacd",
]


def _main():
    parser = argparse.ArgumentParser(
        prog="retroarch-orchestrator",
        description="Run retroarch with optional steps/configuration automtically applied",
    )
    parser.add_argument(
        "args",
        nargs="*",
    )

    args = parser.parse_args()
    final_command = []
    final_command.extend(["savepath-injector.py", "--"])
    config_path = utils.get_ra_config_path(args.args)
    system = utils.get_ra_system_from_path(config_path)
    if system in _XDELTA_PATCHER_SYSTEMS:
        # the rom probably won't be the last argument, so figure it out and pass it explicitly'
        rom = _get_rom_path(args.args[1:])
        final_command.extend(["xdelta-patcher.py", "-f", rom, "--"])
    # add actual command
    final_command.extend(args.args)
    # print(f"{final_command}")
    subprocess.run(final_command, check=True)


if __name__ == "__main__":
    _main()
