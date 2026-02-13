#!/usr/bin/python3

import argparse
import os
import os.path
import sys

import utils


def _check_tracklist_file(track_file, iterate_fn):
    track_path = os.path.dirname(track_file)
    missing = []

    def _track_cb(track_part):
        tp = os.path.join(track_path, track_part)
        if not os.path.exists(tp):
            missing.append(track_part)

    iterate_fn(track_file, _track_cb)
    if missing:
        return [(track_file, missing)]
    return []


def _check_gdi(filename):
    return _check_tracklist_file(filename, utils.iterate_gdi_tracks)


def _check_cue(filename):
    return _check_tracklist_file(filename, utils.iterate_cue_tracks)


def _check_m3u(filename):
    m3u_path = os.path.dirname(filename)
    missing_chunks = []
    ret = []

    def _cb(m3u_part):
        chunk_path = os.path.join(m3u_path, m3u_part)
        if not os.path.exists(chunk_path):
            # print(f"Missing m3u_part: {m3u_part}")
            missing_chunks.append(m3u_part)
        else:
            r = _check_file(chunk_path)
            ret.extend(r)

    utils.iterate_m3u_files(filename, _cb)
    if missing_chunks:
        # print(f"f={filename} mc={missing_chunks}")
        ret.append((filename, missing_chunks))
    return ret


_MULTIFILE_EXTENSIONS = {
    ".cue": _check_cue,
    ".gdi": _check_gdi,
    ".m3u": _check_m3u,
}


def _check_file(filename):
    _, ext = os.path.splitext(filename)
    ext_fn = _MULTIFILE_EXTENSIONS.get(ext)
    if ext_fn:
        return ext_fn(filename)
    # not a multifile; done
    return []


def main():
    parser = argparse.ArgumentParser(
        prog="multifile-validator",
        description="Validate games composed of multiple files have all referenced files available",
    )
    parser.add_argument(
        "files",
        nargs="*",
    )
    args = parser.parse_args()
    missing = []
    for f in args.files:
        m = _check_file(f)
        missing.extend(m)

    if not missing:
        # happy case, no missing files
        sys.exit(0)
    for m in missing:
        print(f"{m[0]} references missing files: {m[1]}")
    sys.exit(1)


if __name__ == "__main__":
    main()
