#!/usr/bin/python3

import argparse
import glob
import os
import os.path
import re
import shutil
import subprocess
import sys

_DEFAULT_SCRATCH = "/mnt/scratch"


def _do_xdelta(base_file, patch_file, scratch):
    basename = os.path.basename(base_file)
    out_file = os.path.join(scratch, basename)
    subprocess.run(
        [
            "xdelta3",
            "-d",
            "-s",
            base_file,
            patch_file,
            out_file,
        ],
        check=True,
    )
    return out_file


def _make_symlinks(target_list, scratch):
    links = []
    for f in target_list:
        target_link = os.path.join(scratch, os.path.basename(f))
        if not os.path.exists(target_link):
            links.append(target_link)
            os.symlink(f, target_link)
    return links


_CUE_FILE_PATTERN = re.compile(r'^FILE\s+"(.*)"')


def _patch_cue(filename, scratch):
    cue_dir = os.path.dirname(filename)
    skipped = []
    patched = []
    with open(filename, "r") as cue_file:
        for line in cue_file:
            m = _CUE_FILE_PATTERN.match(line)
            if m:
                cue_part = os.path.join(cue_dir, m.group(1))
                base, ext = os.path.splitext(cue_part)
                patch_file = base + ".xdelta"
                if os.path.exists(patch_file):
                    out_file = _do_xdelta(cue_part, patch_file, scratch)
                    patched.append(out_file)
                else:
                    skipped.append(cue_part)
    # see if we patched anything
    if patched:
        # make symlinks for everything we skipped
        launch_file = os.path.join(scratch, os.path.basename(filename))
        os.symlink(filename, launch_file)
        to_clean = [launch_file]
        to_clean.extend(patched)
        to_clean.extend(_make_symlinks(skipped, scratch))

        # make symlinks for any files with the same naming pattern; this make sure things like memory cards area available
        base, _ = os.path.splitext(filename)
        possible_links = glob.glob(os.path.join(cue_dir, base) + ".*")
        to_clean.extend(_make_symlinks(possible_links, scratch))
        return True, to_clean
    return False, [filename].extend(skipped)


def _patch_m3u(filename, scratch):
    m3u_dir = os.path.dirname(filename)
    skipped = []
    patched = []
    entries = []
    with open(filename, "r") as m3u_file:
        for line in m3u_file:
            m3u_chunk = line.rstrip()
            real_file = os.path.join(m3u_dir, m3u_chunk)
            p, to_clean = patch_file(real_file, scratch)
            if p:
                patched.extend(to_clean)
            else:
                skipped.extend(to_clean)
            entries.append(os.path.basename(m3u_chunk))
    if patched:
        # something got patched, so make a new m3u
        m3u_path = os.path.join(scratch, os.path.basename(filename))
        with open(m3u_path, "w") as new_m3u:
            new_m3u.write("\n".join(entries))

        # now make symlinks for everything that wasn't patched'
        to_clean = [m3u_path]
        to_clean.extend(patched)
        to_clean.extend(_make_symlinks(skipped, scratch))
        base, _ = os.path.splitext(filename)
        possible_links = glob.glob(os.path.join(m3u_dir, base) + ".*")
        to_clean.extend(_make_symlinks(possible_links, scratch))
        return True, to_clean
    return False, [filename]


_SPECIAL_EXTENSIONS = {
    ".cue": _patch_cue,
    ".m3u": _patch_m3u,
}


def patch_file(filename, scratch):
    base, ext = os.path.splitext(filename)
    ext_fn = _SPECIAL_EXTENSIONS.get(ext)
    if ext_fn:
        return ext_fn(filename, scratch)
    # not special cased
    patch_file = base + ".xdelta"
    if os.path.exists(patch_file):
        out_file = _do_xdelta(filename, patch_file, scratch)
        return True, [out_file]
    return False, [filename]


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
    patched, target = patch_file(args.filename, args.scratch)

    if args.args:
        # everything is patched, execute
        args.args.append(target[0])
        subprocess.run(args.args)

    if patched:
        ex_files = None
        if not args.preserve:
            for f in target:
                os.remove(f)
            # anything left needs to be copied back to the original folder
            ex_files = os.listdir(args.scratch)
        else:
            ex_files = os.listdir(args.scratch)
            for f in target:
                entry = os.path.basename(f)
                try:
                    ex_files.remove(entry)
                except ValueError:
                    # don't care, we'll just copy it back
                    pass
        if ex_files:
            target_dir = os.path.dirname(args.filename)
            for f in ex_files:
                full_file = os.path.join(args.scratch, f)
                shutil.copy(full_file, target_dir)
                os.remove(full_file)


if __name__ == "__main__":
    main()
