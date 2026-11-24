from dataclasses import dataclass
import os.path

import rph_files


@dataclass
class PatchInfo:
    files_to_patch: list[str]
    files_to_modify: list[str]
    files_to_link: list[str]

    def __init__(self):
        self.files_to_patch = []
        self.files_to_modify = []
        self.files_to_link = []


def _check_patch(filename, extension, pi):
    base, _ = os.path.splitext(filename)
    patch_file = f"{base}.{extension}"
    if os.path.exists(patch_file):
        pi.files_to_patch.append(filename)
    else:
        pi.files_to_link.append(filename)


def _build_trackfile_info(iterate_fn, filename, patch_extension):
    real_dir = os.path.realpath(os.path.dirname(filename))
    must_modify = False
    ret = PatchInfo()

    def _cb(track_part):
        nonlocal must_modify
        nonlocal ret

        tpd = os.path.dirname(track_part)
        if tpd:
            part_dir = os.path.realpath(os.path.dirname(track_part))
            if part_dir != real_dir:
                must_modify = True
        _check_patch(os.path.join(real_dir, track_part), patch_extension, ret)

    iterate_fn(filename, _cb)
    if must_modify:
        ret.files_to_modify.append(filename)
    else:
        ret.files_to_link.append(filename)
    return ret


def _build_trackfile_fn(iterate_fn):
    return lambda f, pe: _build_trackfile_info(iterate_fn, f, pe)


def _build_m3u_info(filename, patch_extension):
    real_dir = os.path.realpath(os.path.dirname(filename))
    must_modify = False
    ret = PatchInfo()

    def _cb(m3u_part):
        nonlocal must_modify

        mpd = os.path.dirname(m3u_part)
        if mpd:
            part_dir = os.path.realpath(mpd)
            if part_dir != real_dir:
                must_modify = True
        part_pi = build_patch_info(os.path.join(real_dir, m3u_part), patch_extension)
        ret.files_to_patch.extend(part_pi.files_to_patch)
        ret.files_to_modify.extend(part_pi.files_to_modify)
        ret.files_to_link.extend(part_pi.files_to_link)

    rph_files.iterate_m3u_files(filename, _cb)
    if must_modify:
        ret.files_to_modify.append(filename)
    else:
        ret.files_to_link.append(filename)
    return ret


_SPECIAL_EXTENSIONS = {
    ".cue": _build_trackfile_fn(rph_files.iterate_cue_tracks),
    ".gdi": _build_trackfile_fn(rph_files.iterate_gdi_tracks),
    ".m3u": _build_m3u_info,
}


def build_patch_info(filename, patch_extension):
    _, ext = os.path.splitext(filename)
    ext_fn = _SPECIAL_EXTENSIONS.get(ext)
    if ext_fn:
        return ext_fn(filename, patch_extension)
    # not special cased
    ret = PatchInfo()
    _check_patch(filename, patch_extension, ret)
    return ret


def _rewrite_m3u(original, target):
    with open(target, "w", encoding="utf-8") as new_m3u:

        def _write_entry(entry):
            new_m3u.write(f"{entry}\n")

        rph_files.iterate_m3u_files(original, _write_entry)


_MODIFIER_FNS = {
    # ".cue": _rewrite_cue
    # ".gdi": _rewrite_gdi
    ".m3u": _rewrite_m3u,
}


def do_patch_work(pi, work_dir, patch_fn):
    for f in pi.files_to_patch:
        patch_fn(f)
    for f in pi.files_to_link:
        out_file = os.path.join(work_dir, os.path.basename(f))
        os.symlink(f, out_file)
    for f in pi.files_to_modify:
        _, ext = os.path.splitext(f)
        fn = _MODIFIER_FNS.get(ext)
        if fn:
            target = os.path.join(work_dir, os.path.basename(f))
            fn(f, target)
        else:
            raise RuntimeError(f"Unknown extentension to modify: {ext}")
