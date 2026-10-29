#!/usr/bin/python3

import argparse
import os.path


def _get_memcard_path(game, save_extension):
    base, _ = os.path.splitext(os.path.basename(game))
    return f"{base}.{save_extension}"


def main():
    parser = argparse.ArgumentParser(
        prog="setup-shared-memcard",
        description="Create symlinks to share a memory card file",
    )
    parser.add_argument(
        "-p",
        "--parent",
        help="Game associated with the actual memory card",
        required=True,
    )
    parser.add_argument(
        "-s",
        "--suffix",
        help="Suffix for a memory card (i.e., extension)",
        default="srm",
    )
    parser.add_argument(
        "-d",
        "--save-directory",
        help="Memory card directory (by default same directory as game)",
    )
    parser.add_argument(
        "games",
        nargs="*",
    )
    args = parser.parse_args()
    parent_save = _get_memcard_path(args.parent, args.suffix)
    save_path = parent_save
    parent_dir = os.path.dirname(args.parent)
    if not args.save_directory:
        save_path = os.path.join(parent_dir, parent_save)
    for game in args.games:
        linked_save = _get_memcard_path(game, args.suffix)
        to_link = parent_save
        if args.save_directory:
            linked_path = os.path.join(args.save_directory, linked_save)
        else:
            game_dir = os.path.dirname(game)
            linked_path = os.path.join(game_dir, linked_save)
            if game_dir != parent_dir:
                to_link = os.path.abspath(save_path)
        if not os.path.exists(linked_path):
            os.symlink(to_link, linked_path)


if __name__ == "__main__":
    main()
