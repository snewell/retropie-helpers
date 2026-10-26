#!/usr/bin/python3

import argparse
import os
import os.path


def _get_system_list(system_dir):
    ret = []
    with os.scandir(system_dir) as it:
        for entry in it:
            if not entry.name.startswith(".") and entry.is_dir():
                ret.append(entry.name)
    return ret


def _make_dirs(system_list, base_dir):
    for s in system_list:
        fp = os.path.join(base_dir, s)
        if not os.path.isdir(fp):
            os.makedirs(fp, mode=0o755)


def main():
    parser = argparse.ArgumentParser(
        prog="make-save-folders",
        description="Create folders for save data",
    )
    parser.add_argument(
        "-s",
        "--save-dir",
        help="Folder to create individual save folders",
        required=True,
    )
    parser.add_argument(
        "-l",
        "--system-list-dir",
        help="A folder that contains the list of supported systems (e.g., rom folder)",
        default="/opt/retropie/configs",
    )
    args = parser.parse_args()
    systems = _get_system_list(args.system_list_dir)
    _make_dirs(systems, args.save_dir)


if __name__ == "__main__":
    main()
