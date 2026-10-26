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


def _setup_card_links(romfile, memcards, savedir):
    base, _ = os.path.splitext(os.path.basename(romfile))
    for m, l in memcards:
        save_path = os.path.join(savedir, f"{base}.{l}")
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
        "--save-dir",
        help="Path for per-game memory cards (defaults to content directory)",
    )
    parser.add_argument(
        "-e",
        "--srm8-extension",
        help="Extension for an 8MB per-game memory card",
        default="srm8",
    )
    parser.add_argument(
        "-E",
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
    rom_dir = os.path.dirname(args.filename)
    if args.save_dir is None:
        args.save_dir = rom_dir
    if args.memcard8_path is None:
        args.memcard8_path = os.path.join(rom_dir, _DEFAULT_CARD_DIR, _SHARED_MEMCARD8)
    if args.memcard32_path is None:
        args.memcard32_path = os.path.join(
            rom_dir, _DEFAULT_CARD_DIR, _SHARED_MEMCARD32
        )

    memcards = [
        (args.memcard8_path, args.srm8_extension),
        (args.memcard32_path, args.srm32_extension),
    ]
    _verify_no_cards(memcards)
    _setup_card_links(args.filename, memcards, args.save_dir)

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
