import pathlib
import re
import shlex


def _iterate_tracklist_file(filename, pattern, track_cb):
    with open(filename, "r", encoding="utf-8") as track_file:
        for line in track_file:
            m = pattern.match(line)
            if m:
                track_cb(m.group(1))


_CUE_FILE_PATTERN = re.compile(r'^\s*FILE\s+"([^"]+)"', re.IGNORECASE)


def iterate_cue_tracks(filename, track_cb):
    _iterate_tracklist_file(filename, _CUE_FILE_PATTERN, track_cb)


def iterate_gdi_tracks(filename, track_cb):
    with open(filename, "r", encoding="utf-8") as track_file:
        for line in track_file:
            cleaned_line = line.strip()
            if cleaned_line:
                tokens = shlex.split(cleaned_line)

                # A valid GDI track row strictly requires at least 6 standard columns:
                # Tracknum, Start-Sector, Mode, Sector-Size, Filename, Filename-Offset
                if len(tokens) >= 6 and tokens[0].isdigit():
                    filename_token = tokens[4]
                    track_cb(filename_token)


def iterate_m3u_files(filename, file_cb):
    with open(filename, "r", encoding="utf-8") as m3u_file:
        for line in m3u_file:
            cleaned_line = line.strip()
            # Explicitly ignore empty lines and metadata/comment tags
            if not cleaned_line or cleaned_line.startswith("#"):
                continue
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
