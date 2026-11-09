import unittest
from unittest.mock import patch, mock_open

import rph_files


class TestRphFiles(unittest.TestCase):
    def test_cue_handles_lowercase_and_whitespace(self):
        cue_data = '  file "Track_01.bin" BINARY\nFILE "Track_02.img" WAVE'
        captured = []

        with patch("builtins.open", mock_open(read_data=cue_data)), patch(
            "os.path.isfile", return_value=True
        ):
            rph_files.iterate_cue_tracks("game.cue", captured.append)

        self.assertEqual(captured, ["Track_01.bin", "Track_02.img"])

    def test_gdi_strips_quotes_from_filenames_with_spaces(self):
        # Line 1 has no quotes, Line 2 has quotes protecting a filename with spaces
        gdi_data = (
            "1 0 4 2352 track01.bin 0\n"
            '2 150 0 2352 "track 02.raw" 0\n'
            "3   450   0   2352   track03.bin   0"
        )
        captured = []

        with patch("builtins.open", mock_open(read_data=gdi_data)), patch(
            "os.path.isfile", return_value=True
        ):
            rph_files.iterate_gdi_tracks("game.gdi", captured.append)

        self.assertEqual(captured, ["track01.bin", "track 02.raw", "track03.bin"])

    def test_m3u_skips_comments_and_empty_lines(self):
        m3u_data = "#EXTM3U\n#EXTINF:Disc 1\nDisc1.iso\n\nDisc2.iso\n"
        captured = []

        with patch("builtins.open", mock_open(read_data=m3u_data)), patch(
            "os.path.isfile", return_value=True
        ):
            rph_files.iterate_m3u_files("playlist.m3u", captured.append)

        self.assertEqual(captured, ["Disc1.iso", "Disc2.iso"])


if __name__ == "__main__":
    unittest.main()
