"""
Test the configuration loader.

The loader is responsible for loading the fookebox configuration file and for
providing reasonable default values.
"""

from unittest import TestCase
from fookebox.config import load_config, default_config


class TestConfigLoader(TestCase):
    # pylint: disable=missing-class-docstring
    def test_load_empty_config(self) -> None:
        """Load an empty configuration file. All values should be set."""
        cfg = load_config('tests/fixtures/config-empty.ini')

        self.assertEqual(cfg.get('site_name'), "fookebox")
        self.assertEqual(cfg.getint('listen_port'), 8888)
        self.assertEqual(cfg.get('mpd_host'), "localhost")
        self.assertEqual(cfg.getint('mpd_port'), 6600)
        self.assertIsNone(cfg.get('mpd_pass'))
        self.assertEqual(cfg.getint('max_queue_length'), 5)
        self.assertTrue(cfg.getboolean('auto_queue'))
        self.assertEqual(cfg.getint('auto_queue_time_left'), 3)
        self.assertIsNone(cfg.get('auto_queue_playlist'))
        self.assertIsNone(cfg.get('auto_queue_genre'))
        self.assertTrue(cfg.getboolean('show_search'))
        self.assertTrue(cfg.getboolean('enable_controls'))
        self.assertTrue(cfg.getboolean('enable_song_removal'))
        self.assertTrue(cfg.getboolean('enable_queue_album'))

    def test_load_config_without_fookebox_section(self) -> None:
        """Load a configuration file without a fookebox section.
           All values should be set."""
        cfg = load_config('tests/fixtures/config-no-fookebox-section.ini')

        self.assertEqual(cfg.get('site_name'), "fookebox")
        self.assertEqual(cfg.getint('listen_port'), 8888)
        self.assertEqual(cfg.get('mpd_host'), "localhost")
        self.assertEqual(cfg.getint('mpd_port'), 6600)
        self.assertIsNone(cfg.get('mpd_pass'))
        self.assertEqual(cfg.getint('max_queue_length'), 5)
        self.assertTrue(cfg.getboolean('auto_queue'))
        self.assertEqual(cfg.getint('auto_queue_time_left'), 3)
        self.assertIsNone(cfg.get('auto_queue_playlist'))
        self.assertIsNone(cfg.get('auto_queue_genre'))
        self.assertTrue(cfg.getboolean('show_search'))
        self.assertTrue(cfg.getboolean('enable_controls'))
        self.assertTrue(cfg.getboolean('enable_song_removal'))
        self.assertTrue(cfg.getboolean('enable_queue_album'))

    def test_load_default_config(self) -> None:
        """Load default settings"""
        cfg = default_config()

        self.assertEqual(cfg.get('site_name'), "fookebox")
        self.assertEqual(cfg.getint('listen_port'), 8888)
        self.assertEqual(cfg.get('mpd_host'), "localhost")
        self.assertEqual(cfg.getint('mpd_port'), 6600)
        self.assertIsNone(cfg.get('mpd_pass'))
        self.assertEqual(cfg.getint('max_queue_length'), 5)
        self.assertTrue(cfg.getboolean('auto_queue'))
        self.assertEqual(cfg.getint('auto_queue_time_left'), 3)
        self.assertIsNone(cfg.get('auto_queue_playlist'))
        self.assertIsNone(cfg.get('auto_queue_genre'))
        self.assertTrue(cfg.getboolean('show_search'))
        self.assertTrue(cfg.getboolean('enable_controls'))
        self.assertTrue(cfg.getboolean('enable_song_removal'))
        self.assertTrue(cfg.getboolean('enable_queue_album'))

    def test_load_some_config(self) -> None:
        """Load a configuration file. All values should be set."""
        cfg = load_config('tests/fixtures/config-example-1.ini')

        self.assertEqual(cfg.get('site_name'), "test site 1")
        self.assertEqual(cfg.getint('listen_port'), 8889)
        self.assertEqual(cfg.get('mpd_host'), "test host")
        self.assertEqual(cfg.getint('mpd_port'), 612)
        self.assertEqual(cfg.get('mpd_pass'), "test password")
        self.assertEqual(cfg.getint('max_queue_length'), 7)
        self.assertTrue(cfg.getboolean('auto_queue'))
        self.assertEqual(cfg.getint('auto_queue_time_left'), 19)
        self.assertEqual(cfg.get('auto_queue_playlist'), "idle")
        self.assertEqual(cfg.get('auto_queue_genre'), "Jazz")
        self.assertTrue(cfg.getboolean('show_search'))
        self.assertTrue(cfg.getboolean('enable_controls'))
        self.assertTrue(cfg.getboolean('enable_song_removal'))
        self.assertTrue(cfg.getboolean('enable_queue_album'))

    def test_load_other_config(self) -> None:
        """Load a different configuration file. All values should be set."""
        cfg = load_config('tests/fixtures/config-example-2.ini')

        self.assertEqual(cfg.get('site_name'), "test site 2")
        self.assertEqual(cfg.getint('listen_port'), 8890)
        self.assertEqual(cfg.get('mpd_host'), "mpd host")
        self.assertEqual(cfg.getint('mpd_port'), 613)
        self.assertEqual(cfg.get('mpd_pass'), "password")
        self.assertEqual(cfg.getint('max_queue_length'), 6)
        self.assertFalse(cfg.getboolean('auto_queue'))
        self.assertEqual(cfg.getint('auto_queue_time_left'), 20)
        self.assertEqual(cfg.get('auto_queue_playlist'), "playlist")
        self.assertEqual(cfg.get('auto_queue_genre'), "Rock & Roll")
        self.assertFalse(cfg.getboolean('show_search'))
        self.assertFalse(cfg.getboolean('enable_controls'))
        self.assertFalse(cfg.getboolean('enable_song_removal'))
        self.assertFalse(cfg.getboolean('enable_queue_album'))
