import os
import os.path
import unittest
from unittest.mock import mock_open, patch

import rph_patch


def _prepend_cwd(args):
    ret = []
    for a in args:
        ret.append(os.path.join(os.getcwd(), a))
    return ret


class TestRphPatch(unittest.TestCase):
    def test_patch_does_not_exist(self):
        pi = None
        filename = "Game.iso"
        with patch("os.path.exists", return_value=False):
            pi = rph_patch.build_patch_info(filename, "xdelta")

        self.assertEqual(pi.files_to_patch, [])
        self.assertEqual(pi.files_to_modify, [])
        self.assertEqual(pi.files_to_link, [filename])

    def test_patch_does_exists(self):
        pi = None
        filename = "Game.iso"
        with patch("os.path.exists", return_value=True):
            pi = rph_patch.build_patch_info(filename, "xdelta")

        self.assertEqual(pi.files_to_patch, [filename])
        self.assertEqual(pi.files_to_modify, [])
        self.assertEqual(pi.files_to_link, [])

    def test_cue_with_no_patch(self):
        pi = None
        filename = "Game.cue"
        track1 = "Track1.bin"
        cue_data = f'FILE "{track1}" BINARY'
        with patch("os.path.exists", return_value=False), patch(
            "builtins.open", mock_open(read_data=cue_data)
        ):
            pi = rph_patch.build_patch_info(filename, "xdelta")

        self.assertEqual(pi.files_to_patch, [])
        self.assertEqual(pi.files_to_modify, [])
        self.assertEqual(pi.files_to_link, _prepend_cwd([track1]) + [filename])

    def test_gdi_with_no_patch(self):
        pi = None
        filename = "Game.gdi"
        track1 = "Track01.bin"
        track2 = "Track 02.bin"
        gdi_data = f"1 0 4 2352 {track1} 0\n" f'2 150 0 2352 "{track2}" 0\n'
        with patch("os.path.exists", return_value=False), patch(
            "builtins.open", mock_open(read_data=gdi_data)
        ):
            pi = rph_patch.build_patch_info(filename, "xdelta")

        self.assertEqual(pi.files_to_patch, [])
        self.assertEqual(pi.files_to_modify, [])
        self.assertEqual(pi.files_to_link, _prepend_cwd([track1, track2]) + [filename])

    def test_m3u_with_no_patch(self):
        pi = None
        filename = "Game.m3u"

        disc1 = "Disc 1.iso"
        disc2 = "Disc 2.iso"
        m3u_data = f"{disc1}\n{disc2}"
        with patch("os.path.exists", return_value=False), patch(
            "builtins.open", mock_open(read_data=m3u_data)
        ):
            pi = rph_patch.build_patch_info(filename, "xdelta")

        self.assertEqual(pi.files_to_patch, [])
        self.assertEqual(pi.files_to_modify, [])
        self.assertEqual(pi.files_to_link, _prepend_cwd([disc1, disc2]) + [filename])

    def test_m3u_with_different_dir(self):
        pi = None
        filename = "Game.m3u"

        disc1 = "somedir/Disc 1.iso"
        disc2 = "somedir/Disc 2.iso"
        m3u_data = f"{disc1}\n{disc2}"
        with patch("os.path.exists", return_value=False), patch(
            "builtins.open", mock_open(read_data=m3u_data)
        ):
            pi = rph_patch.build_patch_info(filename, "xdelta")

        self.assertEqual(pi.files_to_patch, [])
        self.assertEqual(pi.files_to_modify, [filename])
        self.assertEqual(pi.files_to_link, _prepend_cwd([disc1, disc2]))

    def test_m3u_with_everything_patched(self):
        pi = None
        filename = "Game.m3u"

        disc1 = "Disc 1.iso"
        disc2 = "Disc 2.iso"
        m3u_data = f"{disc1}\n{disc2}"
        with patch("os.path.exists", return_value=True), patch(
            "builtins.open", mock_open(read_data=m3u_data)
        ):
            pi = rph_patch.build_patch_info(filename, "xdelta")

        self.assertEqual(pi.files_to_patch, _prepend_cwd([disc1, disc2]))
        self.assertEqual(pi.files_to_modify, [])
        self.assertEqual(pi.files_to_link, [filename])

    def test_m3u_with_partial_patched(self):
        pi = None
        filename = "Game.m3u"

        disc1 = "Disc 1.iso"
        disc2 = "Disc 2.iso"
        m3u_data = f"{disc1}\n{disc2}"

        def _exists_mock(exists_filename):
            return os.path.basename(exists_filename) == "Disc 1.xdelta"

        with patch("os.path.exists", side_effect=_exists_mock), patch(
            "builtins.open", mock_open(read_data=m3u_data)
        ):
            pi = rph_patch.build_patch_info(filename, "xdelta")

        self.assertEqual(pi.files_to_patch, _prepend_cwd([disc1]))
        self.assertEqual(pi.files_to_modify, [])
        self.assertEqual(pi.files_to_link, _prepend_cwd([disc2]) + [filename])


if __name__ == "__main__":
    unittest.main()
