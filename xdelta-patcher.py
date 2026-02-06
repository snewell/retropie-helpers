#!/usr/bin/python3

import argparse
import os
import os.path
import subprocess
import sys

_DEFAULT_SCRATCH = "/mnt/scratch"


def patch_file(args):
    base, ext = os.path.splitext(args.filename)
    patch_file = base + ".xdelta"
    if os.path.exists(patch_file):
        basename = os.path.basename(args.filename)
        out_file = os.path.join(args.scratch, basename)
        subprocess.run(
            [
                "xdelta3",
                "-d",
                "-s",
                args.filename,
                patch_file,
                out_file,
            ],
            check=True,
        )
        return True, out_file
    return False, args.filename


def main():
    parser = argparse.ArgumentParser(
        prog="xdelta-patcher",
        description="Apply available xdelta patches before launching emulator",
    )
    parser.add_argument(
        "-p",
        "--preserve",
        action="store_true",
        help="Don't clean scratch directory",
    )
    parser.add_argument("-s", "--scratch", help="Scratch directory to use")
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
    if args.scratch is None:
        args.scratch = _DEFAULT_SCRATCH
    if args.filename is None:
        # try to steal the last floating argument
        if len(args.args) < 1:
            print("Error: no filename and no args to steal from", file=sys.stderr)
            exit(1)
        args.filename = args.args[-1]
        args.args = args.args[:-1]
    to_clean = []
    patched, target = patch_file(args)
    if patched:
        to_clean.append(target)

    if args.args:
        # everything is patched, execute
        args.args.append(target)
        subprocess.run(args.args)

    if not args.preserve and to_clean:
        for f in to_clean:
            os.remove(f)


if __name__ == "__main__":
    main()
