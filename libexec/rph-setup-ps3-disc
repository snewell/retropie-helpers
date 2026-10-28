#!/usr/bin/python3

import argparse
import os
import os.path
import subprocess

import utils

_DEFAULT_MOUNT_POINT = "/mnt/ps3-disc"


def _mount(game_file, mount_dir):
    subprocess.run(
        [
            "fuseiso",
            "-p",  # create/remove mount point automatically
            game_file,
            mount_dir,
        ],
        check=True,
    )


def _unmount(mount_dir):
    subprocess.run(
        [
            "fusermount",
            "-u",
            mount_dir,
        ],
        check=True,
    )


def _make_game_path(base_dir):
    return os.path.join(base_dir, "PS3_GAME", "USRDIR", "EBOOT.BIN")


def _setup_game(game_path, mount_dir):
    if os.path.isfile(game_path):
        # regular file, assume it's a disc'
        def _mount_and_run(run_fn):
            _mount(game_path, mount_dir)
            run_file = _make_game_path(mount_dir)
            try:
                run_fn(run_file)
            finally:
                _unmount(mount_dir)

        return _mount_and_run
    if os.path.isdir(game_path):
        # for some reason it's a real directory'
        return lambda run_fn: run_fn(_make_game_path(game_path))
    if os.path.islink(game_path):
        # it's a link, so recurse
        target = os.readlink(game_path)
        if not os.path.isabs(target):
            # Reconstruct the true absolute destination relative to the link's home folder
            target = os.path.normpath(os.path.join(os.path.dirname(game_path), target))

        return _setup_game(os.readlink(game_path), mount_dir)
    raise RuntimeError("Unexpected type of file")


def _make_execute_fn(args, original_path):
    def _run_fn(run_path):
        utils.replace_args(args, original_path, run_path)
        subprocess.run(args, check=True)

    return _run_fn


def _main():
    parser = argparse.ArgumentParser(
        prog="setup-ps3-disc",
        description="Determine the proper path to a PS3 game, mounting a disc if necessary",
    )
    parser.add_argument("-m", "--mount-point", help="Mount point for discs")
    parser.add_argument(
        "-f",
        "--filename",
        help="File to patch",
    )
    parser.add_argument(
        "args",
        nargs="*",
    )

    args = parser.parse_args()
    if args.mount_point is None:
        args.mount_point = _DEFAULT_MOUNT_POINT
    args.mount_point = os.path.join(args.mount_point, str(os.getpid()))

    args.filename, args.args = utils.get_filename_and_args(args.filename, args.args)
    run_fn = _setup_game(args.filename, args.mount_point)
    if args.args:
        execute_fn = _make_execute_fn(args.args, args.filename)
        run_fn(execute_fn)


if __name__ == "__main__":
    _main()
