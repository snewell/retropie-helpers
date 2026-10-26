import pathlib
import re


def _iterate_tracklist_file(filename, pattern, track_cb):
    with open(filename, "r", encoding="utf-8") as track_file:
        for line in track_file:
            m = pattern.match(line)
            if m:
                track_cb(m.group(1))


_CUE_FILE_PATTERN = re.compile(r'^FILE\s+"(.*)"')


def iterate_cue_tracks(filename, track_cb):
    _iterate_tracklist_file(filename, _CUE_FILE_PATTERN, track_cb)


_GDI_FILE_PATTERN = re.compile(r"\d+\s+\d+\s+\d+\s+\d+\s+(.*)\s+\d+")


def iterate_gdi_tracks(filename, track_cb):
    _iterate_tracklist_file(filename, _GDI_FILE_PATTERN, track_cb)


def iterate_m3u_files(filename, file_cb):
    with open(filename, "r", encoding="utf-8") as m3u_file:
        for line in m3u_file:
            file_cb(line.rstrip())


def get_filename_and_args(filename, args):
    if filename is None:
        # try to steal the last floating argument
        if len(args) < 1:
            raise RuntimeError("Error: no filename and no args to steal from")
        return (args[-1], args[:-1])
    return (filename, args)


def replace_args(args, target, replacement):
    # everything is patched, execute
    replaced = False
    for i in range(len(args)):
        if args[i] == target:
            args[i] = replacement
            replaced = True
    if not replaced:
        args.append(replacement)
    return args


def get_ra_config_path(args):
    config_idx = args.index("--config")
    # if this is out of range, we've got a weird command line; okay to crash, just check the logs
    return args[config_idx + 1]


def get_ra_system_from_path(file_path):
    # this assumes config/roms live in folders with default names
    p = pathlib.Path(file_path)
    return p.parent.name
