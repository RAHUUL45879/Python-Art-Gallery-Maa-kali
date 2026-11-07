import sys
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
import render_radiant_31s as film
from code_art import scene1, scene3

class RadiantFilmTests(unittest.TestCase):
    def test_timing(self):
        self.assertEqual(film.OPENING,152)
        self.assertEqual(film.MIDDLE,354)
        self.assertEqual(film.ENDING,114)
        self.assertEqual(film.FRAMES,620)
    def test_reference_present(self):
        self.assertEqual(len(film.animation_frames()),16)
    def test_opening_unchanged(self):
        self.assertEqual(film.render_frame(98).tobytes(),scene1.render_frame(98).tobytes())
    def test_ending_unchanged(self):
        self.assertEqual(film.render_frame(580).tobytes(),scene3.render_frame(74).tobytes())
    def test_middle_dimensions(self):
        for i in (0,45,115,220,353):
            self.assertEqual(film.middle_frame(i).size,(432,768))
    def test_middle_is_animated(self):
        self.assertNotEqual(film.middle_frame(20).tobytes(),film.middle_frame(220).tobytes())
    def test_bounds(self):
        for i in (-1,620):
            with self.assertRaises(ValueError):film.render_frame(i)
    def test_no_lion(self):
        self.assertFalse(hasattr(film,'draw_lion'))

if __name__=='__main__':unittest.main()
