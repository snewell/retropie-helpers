import re


def _iterate_tracklist_file(filename, pattern, track_cb):
    with open(filename, "r") as track_file:
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
