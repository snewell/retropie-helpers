#!/usr/bin/python3

import argparse
import os.path
import subprocess

import utils

_SHARED_MEMCARD8 = "Mcd001.ps2"
_SHARED_MEMCARD32 = "Shared Memory Card (32 MB).ps2"

_DEFAULT_CARD_DIR = "Slot 1"


def _verify_no_cards(memcards):
    for mcd in memcards:
        if os.path.exists(mcd[0]):
            raise RuntimeError(f"Memory card already exists: {mcd[0]}")


def _setup_card_links(romfile, memcards):
    romdir = os.path.dirname(romfile)
    base, _ = os.path.splitext(romfile)
    for m, l in memcards:
        save_path = os.path.join(romdir, f"{base}.{l}")
        os.symlink(save_path, m)


def main():
    parser = argparse.ArgumentParser(
        prog="unique-memcard",
        description="Provide a unique memory card file for each PCSX2 title",
    )
    parser.add_argument(
        "-f",
        "--filename",
        help="File to execute",
    )
    parser.add_argument(
        "-m", "--memcard8-path", help="Explicit path to emulator's 8MB memory card"
    )
    parser.add_argument(
        "-M", "--memcard32-path", help="Explicit path to emulator's 32MB memory card"
    )
    parser.add_argument(
        "-s",
        "--srm8-extension",
        help="Extension for an 8MB per-game memory card",
        default="srm8",
    )
    parser.add_argument(
        "-S",
        "--srm32-extension",
        help="Extension for an 32MB per-game memory card",
        default="srm32",
    )
    parser.add_argument(
        "args",
        nargs="*",
    )
    args = parser.parse_args()
    args.filename, args.args = utils.get_filename_and_args(args.filename, args.args)
    if args.memcard8_path is None:
        rom_dir = os.path.dirname(args.filename)
        args.memcard8_path = os.path.join(rom_dir, _DEFAULT_CARD_DIR, _SHARED_MEMCARD8)
    if args.memcard32_path is None:
        rom_dir = os.path.dirname(args.filename)
        args.memcard32_path = os.path.join(
            rom_dir, _DEFAULT_CARD_DIR, _SHARED_MEMCARD32
        )

    memcards = [
        (args.memcard8_path, args.srm8_extension),
        (args.memcard32_path, args.srm32_extension),
    ]
    _verify_no_cards(memcards)
    _setup_card_links(args.filename, memcards)

    try:
        if args.args:
            # everything is patched, execute
            args.args.append(args.filename)
            subprocess.run(args.args, check=True)
    finally:
        for m, _ in memcards:
            os.remove(m)


if __name__ == "__main__":
    main()
