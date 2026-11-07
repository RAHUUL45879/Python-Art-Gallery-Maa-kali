"""Fast launcher checks (rendering is mocked; existing tests cover frames)."""
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import play as launcher


class PlayCommandTests(unittest.TestCase):
    def test_no_music_is_allowed(self):
        with tempfile.TemporaryDirectory() as temp:
            with patch.object(launcher, "AUDIO_DIR", Path(temp)):
                self.assertIsNone(launcher.select_music())

    def test_one_music_file_is_detected(self):
        with tempfile.TemporaryDirectory() as temp:
            track = Path(temp) / "song.MP3"
            track.write_bytes(b"test track placeholder")
            with patch.object(launcher, "AUDIO_DIR", Path(temp)):
                self.assertEqual(launcher.select_music(), track)

    def test_multiple_tracks_are_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            (Path(temp) / "a.mp3").touch()
            (Path(temp) / "b.wav").touch()
            with patch.object(launcher, "AUDIO_DIR", Path(temp)):
                with self.assertRaises(ValueError):
                    launcher.select_music()

    def test_silent_render_uses_current_python(self):
        with patch("play.subprocess.run") as run, \
             patch.object(launcher, "SILENT_VIDEO") as out:
            out.is_file.return_value = True
            self.assertEqual(launcher.play(silent=True, no_open=True), 0)
            self.assertEqual(run.call_count, 1)
            command = run.call_args.args[0]
            self.assertEqual(command[0], launcher.sys.executable)
            self.assertTrue(command[1].endswith("render_radiant_31s.py"))

    def test_audio_mix_follows_full_render(self):
        with patch("play.select_music", return_value=Path("song.mp3")), \
             patch("play.subprocess.run") as run, \
             patch.object(launcher, "MUSIC_VIDEO") as out:
            out.is_file.return_value = True
            self.assertEqual(launcher.play(no_open=True), 0)
            self.assertEqual(run.call_count, 2)
            self.assertTrue(run.call_args.args[0][1].endswith("add_music.py"))

    def test_preview_does_not_attempt_music(self):
        with patch("play.select_music") as music, \
             patch("play.subprocess.run") as run, \
             patch.object(launcher, "PREVIEW_VIDEO") as out:
            out.is_file.return_value = True
            self.assertEqual(launcher.play(preview=True, no_open=True), 0)
            music.assert_not_called()
            self.assertEqual(run.call_count, 1)
            self.assertIn("--preview", run.call_args.args[0])


if __name__ == "__main__":
    unittest.main()
