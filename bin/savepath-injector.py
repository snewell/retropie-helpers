#!/usr/bin/python3

import argparse
import os.path
import re
import subprocess

import utils


def _needs_save_injector(config_path):
    with open(config_path, "r", encoding="utf-8") as cf:
        content = cf.read()
        m = re.search(r"^\s*savefile_directory\s*=", content, re.MULTILINE)
        if m:
            return False

    return True


def _write_config(config_path, save_path):
    with open(config_path, "w", encoding="utf-8") as out:
        out.write(f'savefile_directory = "{save_path}"\n')


def _main():
    parser = argparse.ArgumentParser(
        prog="savefile-injector",
        description="Temporarily override the savefile directory in retroarch",
    )
    parser.add_argument("--config-file", help="Specific path to write config file")
    parser.add_argument(
        "--work-dir",
        help="Directory to write temporary file (not used if --config-file is passwed)",
        default="/dev/shm/",
    )
    parser.add_argument(
        "--root-save-dir",
        "-s",
        help="Root directory for save files (per-system save data will be under this)",
        default="/home/pi/saves",
    )
    parser.add_argument(
        "args",
        nargs="*",
    )
    args = parser.parse_args()
    config_path = utils.get_ra_config_path(args.args)
    must_clean = False
    if _needs_save_injector(config_path):
        system = utils.get_ra_system_from_path(config_path)
        if not args.config_file:
            args.config_file = os.path.join(
                args.work_dir, f"ra_save_override_{system}.cfg"
            )
        save_dir = os.path.join(args.root_save_dir, system)
        _write_config(args.config_file, save_dir)
        args.args.extend(["--appendconfig", args.config_file])
        must_clean = True

    try:
        subprocess.run(args.args, check=True)
    finally:
        if must_clean:
            os.remove(args.config_file)


if __name__ == "__main__":
    _main()
