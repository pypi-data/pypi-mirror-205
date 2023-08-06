"""
Test the page template. Make sure it handles translations and configuration
settings correctly.
"""
from importlib import resources
from typing import Optional, Union
from unittest import TestCase

from bs4 import BeautifulSoup
from tornado import locale
from tornado.template import Template

import fookebox

from tests.common import ConfigWrapper


def _load_resource(dir_: str, filename: str) -> str:
    res = resources.files(fookebox).joinpath(dir_)
    with resources.as_file(res) as path:
        src = resources.files(fookebox).joinpath(str(path)).joinpath(filename)
        with resources.as_file(src) as path:
            with open(path, 'r', encoding='utf-8') as file:
                return file.read()


class MockLocale:
    # pylint: disable=too-few-public-methods
    """
    This class is used as a basic no-op locale mock in tests where the locale
    does not matter.
    """
    def __init__(self, code: str = "xx"):
        self.code = code

    @staticmethod
    def translate(val: str) -> str:
        # pylint: disable=missing-function-docstring
        return val


class TestTemplate(TestCase):
    """
    Here we test the page template. The template can show/hide different
    controls based on the configuration.
    """
    @staticmethod
    def render(cfg: ConfigWrapper,
               loc: Union[locale.Locale, MockLocale] = MockLocale(),
               artists: Optional[list[str]] = None,
               genres: Optional[list[str]] = None) -> BeautifulSoup:
        """Render the page template. This is used by other tests"""
        markup = _load_resource('templates', 'client.html')
        template = Template(markup)

        artists = artists or []
        genres = genres or []

        html = template.generate(config=cfg, locale=loc, artists=artists,
                                 genres=genres)
        return BeautifulSoup(html, 'html.parser')

    def test_show_search(self) -> None:
        """Show the search form if 'show_search' has been enabled"""
        config = ConfigWrapper()
        config.set('show_search', True)
        soup = self.render(cfg=config)

        self.assertIsNotNone(soup.find("form", {"id": "artistSearchForm"}))
        self.assertIsNotNone(soup.find("form", {"id": "genreSearchForm"}))

    def test_hide_search(self) -> None:
        """Hide the search form if 'show_search' has not been enabled"""
        config = ConfigWrapper()
        config.set('show_search', False)
        soup = self.render(cfg=config)

        self.assertIsNone(soup.find("form", {"id": "artistSearchForm"}))
        self.assertIsNone(soup.find("form", {"id": "genreSearchForm"}))

    def test_site_name(self) -> None:
        """Use the site_name as page title"""
        config = ConfigWrapper()
        config.set('site_name', 'test 51')
        soup = self.render(cfg=config)
        title = soup.find('title')
        self.assertEqual(title.text, 'test 51')                 # type: ignore

        config.set('site_name', 'other test')
        soup = self.render(cfg=config)
        title = soup.find('title')
        self.assertEqual(title.text, 'other test')              # type: ignore

    def test_enable_controls(self) -> None:
        """Show the control panel controls have been enabled"""
        config = ConfigWrapper()
        config.set('enable_controls', True)
        soup = self.render(cfg=config)
        self.assertIsNotNone(soup.find("div", {"id": "controls"}))

    def test_disable_controls(self) -> None:
        """Hide the control panel controls have not been enabled"""
        config = ConfigWrapper()
        config.set('enable_controls', False)
        soup = self.render(cfg=config)
        self.assertIsNone(soup.find("div", {"id": "controls"}))

    def test_locale_de(self) -> None:
        """Use the German translation"""
        res = resources.files(fookebox).joinpath('i18n')
        with resources.as_file(res) as dir_:
            locale.load_gettext_translations(str(dir_), domain='fookebox')

        soup = self.render(loc=locale.get('de'), cfg=ConfigWrapper())
        link = soup.find("a", {"id": "showArtists"})
        self.assertEqual(link.text, 'Künstler')                 # type: ignore

    def test_locale_en(self) -> None:
        """Use the English language version"""
        res = resources.files(fookebox).joinpath('i18n')
        with resources.as_file(res) as dir_:
            locale.load_gettext_translations(str(dir_), domain='fookebox')

        soup = self.render(loc=locale.get('en'), cfg=ConfigWrapper())
        link = soup.find("a", {"id": "showArtists"})
        self.assertEqual(link.text, 'Artists')                  # type: ignore

    def test_locale_fallback_unknown(self) -> None:
        """Use English as a fallback for unknown languages"""
        res = resources.files(fookebox).joinpath('i18n')
        with resources.as_file(res) as dir_:
            locale.load_gettext_translations(str(dir_), domain='fookebox')

        soup = self.render(loc=locale.get('fr'), cfg=ConfigWrapper())
        link = soup.find("a", {"id": "showArtists"})
        self.assertEqual(link.text, 'Artists')                  # type: ignore

    def test_enable_song_removal(self) -> None:
        """Show the song removal links if song removal has been enabled"""
        config = ConfigWrapper()
        config.set('enable_song_removal', True)

        soup = self.render(cfg=config)
        queue = soup.find("ul", {"id": "queue"})
        controls = queue.find("span", {"class": "controls"})    # type: ignore
        self.assertIsNotNone(controls)

    def test_disable_song_removal(self) -> None:
        """Hide the song removal links if song removal has not been enabled"""
        config = ConfigWrapper()
        config.set('enable_song_removal', False)

        soup = self.render(cfg=config)
        queue = soup.find("ul", {"id": "queue"})
        controls = queue.find("span", {"class": "controls"})    # type: ignore
        self.assertIsNone(controls)

    def test_disable_queue_album(self) -> None:
        """Show the links to queue whole albums if enabled"""
        config = ConfigWrapper()
        config.set('enable_queue_album', False)

        soup = self.render(cfg=config)
        body = soup.find("body")
        self.assertIsNone(body.get("queue-albums"))             # type: ignore

    def test_enable_queue_album(self) -> None:
        """Hide the links to queue whole albums if not enabled"""
        config = ConfigWrapper()
        config.set('enable_queue_album', True)

        soup = self.render(cfg=config)
        body = soup.find("body")
        self.assertEqual(body.get("queue-albums"), "True")      # type: ignore

    def test_artists(self) -> None:
        """Include the list of artists in the page"""
        soup = self.render(cfg=ConfigWrapper(), artists=['The KLF', 'Cher'])
        body = soup.find('body')
        artists = body.find_all('li', {'class': 'artist'})      # type: ignore
        self.assertEqual(len(artists), 2)

    def test_genres(self) -> None:
        """Include the list of genres in the page"""
        soup = self.render(cfg=ConfigWrapper(), genres=['Jazz', 'Funk', 'IDM'])
        body = soup.find('body')
        genres = body.find_all('li', {'class': 'genre'})        # type: ignore
        self.assertEqual(len(genres), 3)
