"""
Test the request handlers

Notably, the handlers should
- accept any type of invalid data without raising any exceptions
- raise HTTP errors when invalid data is sent
- raise HTTP errors when a requested feature has been disabled
"""

from collections.abc import Generator
from json import loads, dumps
from base64 import urlsafe_b64encode
from hashlib import md5
from urllib.parse import quote
from typing import Union

from tornado.httpclient import HTTPResponse
from tornado.web import Application
from tornado.testing import AsyncHTTPTestCase
from bs4 import BeautifulSoup

import tornado

from fookebox.handlers import SocketHandler
from fookebox.mpd import IdleSocket
from fookebox.util import mkapp

from tests.common import ConfigWrapper, MockMPD


class TestQueueHandler(AsyncHTTPTestCase):
    """
    Test the QueueHandler

    This handler has two methods:

    - GET allows the client to load the current queue
    - POST accepts a JSON-encoded list of files to add to the queue

    The POST operation should respect the max_queue_length setting.
    """
    def get_app(self) -> Application:
        # Required override for AsyncHTTPTestCase, sets up a dummy
        # webserver for this test.
        self.mpd = MockMPD()
        self.config = ConfigWrapper()
        return mkapp(self.config, self.mpd, IdleSocket(self.mpd))

    def _post(self, data: str) -> HTTPResponse:
        return self.fetch('/queue', method='POST', body=data)

    def _delete(self, id_: Union[int, str]) -> HTTPResponse:
        return self.fetch(f'/queue/{id_}', method='DELETE')

    def test_post_track(self) -> None:
        """Post a single track (the normal case)"""
        self.assertEqual(self.mpd.mpd_queue, [])
        self.assertEqual(len(self.mpd.commands), 0)

        response = self._post(dumps({'files': ['f1']}))
        self.assertEqual(response.code, 200)
        self.assertEqual(self.mpd.mpd_queue, ['f1'])
        self.assertEqual(len(self.mpd.commands), 1)
        self.assertEqual(self.mpd.commands[0], 'play')

    def test_post_multiple_tracks(self) -> None:
        """Post multiple tracks in a single request (eg. a whole album)"""
        self.assertEqual(self.mpd.mpd_queue, [])
        self.assertEqual(len(self.mpd.commands), 0)

        response = self._post(dumps({'files': ['f1', 'f2', 'f3']}))
        self.assertEqual(response.code, 200)
        self.assertEqual(self.mpd.mpd_queue, ['f1', 'f2', 'f3'])
        self.assertEqual(len(self.mpd.commands), 1)
        self.assertEqual(self.mpd.commands[0], 'play')

    def test_post_track_queue_full(self) -> None:
        """Posting when the queue is full should raise a 409"""
        self.assertEqual(self.mpd.mpd_queue, [])
        self.assertEqual(len(self.mpd.commands), 0)

        self.config.set('max_queue_length', 5)
        self.mpd.mpd_current_song = 'f1'
        self.mpd.mpd_queue = ['f2']

        response = self._post(dumps({'files': ['f3', 'f4', 'f5']}))
        self.assertEqual(response.code, 200)
        self.assertEqual(self.mpd.mpd_queue, ['f2', 'f3', 'f4', 'f5'])

        response = self._post(dumps({'files': ['f6']}))
        self.assertEqual(response.code, 200)
        self.assertEqual(self.mpd.mpd_queue, ['f2', 'f3', 'f4', 'f5', 'f6'])

        response = self._post(dumps({'files': ['f7']}))
        self.assertEqual(response.code, 409)
        self.assertEqual(self.mpd.mpd_queue, ['f2', 'f3', 'f4', 'f5', 'f6'])

    def test_posting_too_many_tracks_fills_queue(self) -> None:
        """Posting too many songs should fill the queue and raise a 409"""
        self.config.set('max_queue_length', 5)
        self.mpd.mpd_current_song = 'f1'

        files = ['f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8']
        response = self._post(dumps({'files': files}))
        self.assertEqual(response.code, 409)
        self.assertEqual(self.mpd.mpd_queue, ['f2', 'f3', 'f4', 'f5', 'f6'])

    def test_post_invalid_data(self) -> None:
        """Accept (and ignore) requests with invalid data"""
        self.assertEqual(len(self.mpd.commands), 0)
        self.assertEqual(self.mpd.mpd_queue, [])

        response = self._post(dumps({'files': 12}))
        self.assertEqual(response.code, 400)
        self.assertEqual(self.mpd.mpd_queue, [])
        self.assertEqual(len(self.mpd.commands), 0)

    def test_post_invalid_json(self) -> None:
        """Accept (and ignore) requests with invalid JSON data"""
        self.assertEqual(len(self.mpd.commands), 0)
        self.assertEqual(self.mpd.mpd_queue, [])

        response = self._post('{"files": ["f1"]')
        self.assertEqual(response.code, 400)
        self.assertEqual(self.mpd.mpd_queue, [])
        self.assertEqual(len(self.mpd.commands), 0)

    def test_post_missing_data(self) -> None:
        """Accept (and ignore) requests without any relevant data"""
        self.assertEqual(len(self.mpd.commands), 0)
        self.assertEqual(self.mpd.mpd_queue, [])

        response = self._post(dumps({'bla': '12'}))
        self.assertEqual(response.code, 200)
        self.assertEqual(self.mpd.mpd_queue, [])

    def test_delete(self) -> None:
        """Delete a song from the queue"""
        self.config.set('enable_song_removal', True)
        self.mpd.mpd_queue = ['A', 'B', 'C', 'D']

        response = self._delete(2)
        self.assertEqual(response.code, 200)
        self.assertEqual(self.mpd.mpd_queue, ['A', 'B', 'D'])

    def test_delete_invalid_url(self) -> None:
        """Delete a song from the queue with a string as id"""
        self.config.set('enable_song_removal', True)
        self.mpd.mpd_queue = ['A', 'B', 'C', 'D']

        response = self._delete('x')
        self.assertEqual(response.code, 404)
        self.assertEqual(self.mpd.mpd_queue, ['A', 'B', 'C', 'D'])

    def test_delete_without_permission(self) -> None:
        """Raise a 403 error when song removal is not allowed"""
        self.config.set('enable_song_removal', False)
        self.mpd.mpd_queue = ['A', 'B', 'C', 'D']

        response = self._delete(2)
        self.assertEqual(response.code, 403)
        self.assertEqual(self.mpd.mpd_queue, ['A', 'B', 'C', 'D'])

    def test_delete_invalid_index(self) -> None:
        """Raise a 400 error when trying to delete an invalid index"""
        self.config.set('enable_song_removal', True)
        self.mpd.mpd_queue = ['A', 'B', 'C', 'D']

        response = self._delete(4)
        self.assertEqual(response.code, 400)
        self.assertEqual(self.mpd.mpd_queue, ['A', 'B', 'C', 'D'])


class TestCoverArtHandler(AsyncHTTPTestCase):
    """
    Test the CoverArtHandler

    The CoverArtHandler fetches album art for a specific file from mpd. It
    expects the file to be passed as a parameter in the URL.

    If cover art is disabled, the handler should raise an HTTP error instead.
    """
    def get_app(self) -> Application:
        # Required override for AsyncHTTPTestCase, sets up a dummy
        # webserver for this test.
        self.mpd = MockMPD()
        self.mpd.mpd_covers = {
            '/media/somebody - my song.mp3': 'blank.png',
            '/media/somebody - second song.mp3': 'blank.jpg'
        }
        self.config = ConfigWrapper()
        return mkapp(self.config, self.mpd, IdleSocket(self.mpd))

    def _get(self, file: str) -> HTTPResponse:
        quoted = quote(file)
        return self.fetch(f'/cover/{quoted}')

    def test_get_cover_that_does_not_exist(self) -> None:
        """Report a 404 error if a cover is not available"""
        response = self._get('/media/somebody - no song.mp3')
        self.assertEqual(response.code, 404)

    def test_get_cover(self) -> None:
        """Load a cover image"""
        response = self._get('/media/somebody - my song.mp3')
        self.assertEqual(response.code, 200)

        encoded = urlsafe_b64encode(response.body)
        self.assertTrue(encoded.startswith(b'iVBOR'))

    def test_get_cover_mime_type(self) -> None:
        """Get and report the correct mime type from a cover image"""
        response = self._get('/media/somebody - my song.mp3')
        self.assertEqual(response.code, 200)
        self.assertEqual(response.headers['Content-Type'], 'image/png')

        response = self._get('/media/somebody - second song.mp3')
        self.assertEqual(response.code, 200)
        self.assertEqual(response.headers['Content-Type'], 'image/jpeg')


class TestControlHandler(AsyncHTTPTestCase):
    """
    Test the ControHandler

    The ControlHandler handles mpd commands such as 'play', 'pause' etc.

    These commands should be forwarded to the backend if controls are enabled
    in the configuration, otherwise the handler should throw an error.
    """
    def get_app(self) -> Application:
        # Required override for AsyncHTTPTestCase, sets up a dummy
        # webserver for this test.
        self.mpd = MockMPD()
        self.mpd.mpd_covers = {
            '/media/somebody - my song.mp3': 'blank.png',
            '/media/somebody - second song.mp3': 'blank.jpg'
        }
        self.config = ConfigWrapper()
        return mkapp(self.config, self.mpd, IdleSocket(self.mpd))

    def _control(self, body: str) -> HTTPResponse:
        return self.fetch('/control', method='POST', body=body)

    def test_controls_disabled(self) -> None:
        """Commands should trigger an HTTP error if controls are disabled"""
        self.config.set('enable_controls', False)
        response = self._control(dumps({'action': 'play'}))

        self.assertEqual(response.code, 403)

    def test_invalid_json(self) -> None:
        """Check that invalid JSON data triggers an HTTP error"""
        self.config.set('enable_controls', True)
        response = self._control('{"action": "bogus"')

        self.assertEqual(response.code, 400)

    def test_missing_command(self) -> None:
        """Check that a request without a command triggers an HTTP error"""
        self.config.set('enable_controls', True)
        response = self._control(dumps({'foo': 'play'}))

        self.assertEqual(response.code, 400)

    def test_invalid_command(self) -> None:
        """Check that invalid comands trigger an HTTP error"""
        self.config.set('enable_controls', True)
        response = self._control(dumps({'action': 'bogus'}))

        self.assertEqual(response.code, 400)

    def test_command_play(self) -> None:
        """Check that the 'play' command is sent to the backend"""
        self.config.set('enable_controls', True)
        response = self._control(dumps({'action': 'play'}))

        self.assertEqual(response.code, 200)
        self.assertEqual(self.mpd.commands, ['play'])

    def test_command_pause(self) -> None:
        """Check that the 'pause' command is sent to the backend"""
        self.config.set('enable_controls', True)
        response = self._control(dumps({'action': 'pause'}))

        self.assertEqual(response.code, 200)
        self.assertEqual(self.mpd.commands, ['pause'])

    def test_command_next(self) -> None:
        """Check that the 'next' command is sent to the backend"""
        self.config.set('enable_controls', True)
        response = self._control(dumps({'action': 'next'}))

        self.assertEqual(response.code, 200)
        self.assertEqual(self.mpd.commands, ['next'])

    def test_command_prev(self) -> None:
        """Check that the 'prev' command is sent to the backend"""
        self.config.set('enable_controls', True)
        response = self._control(dumps({'action': 'prev'}))

        self.assertEqual(response.code, 200)
        self.assertEqual(self.mpd.commands, ['previous'])

    def test_command_volup(self) -> None:
        """Check that the 'volume up' command is sent to the backend"""
        self.config.set('enable_controls', True)
        response = self._control(dumps({'action': 'volup'}))

        self.assertEqual(response.code, 200)
        self.assertEqual(self.mpd.commands, ['volume 10'])

    def test_command_voldown(self) -> None:
        """Check that the 'volume down' command is sent to the backend"""
        self.config.set('enable_controls', True)
        response = self._control(dumps({'action': 'voldown'}))

        self.assertEqual(response.code, 200)
        self.assertEqual(self.mpd.commands, ['volume -10'])

    def test_command_rebuild(self) -> None:
        """Check that the 'rebuild' command is sent to the backend"""
        self.config.set('enable_controls', True)
        response = self._control(dumps({'action': 'rebuild'}))

        self.assertEqual(response.code, 200)
        self.assertEqual(self.mpd.commands, ['update'])


class TestArtistHandler(AsyncHTTPTestCase):
    """
    Test the ArtistHandler

    The artist handler searches MPD for songs by a certain artist and returns
    these songs.

    It should not choke on requests with invalid artist names.
    """
    def get_app(self) -> Application:
        # Required override for AsyncHTTPTestCase, sets up a dummy
        # webserver for this test.
        self.mpd = MockMPD()
        self.mpd.mpd_files.append({'artist': 'The KLF', 'title': '001'})
        self.mpd.mpd_files.append({'artist': 'The KLF', 'title': '002'})
        self.mpd.mpd_files.append({'artist': 'The KLF', 'title': '003'})
        self.mpd.mpd_files.append({'artist': 'The Who', 'title': '004'})
        self.mpd.mpd_files.append({'artist': 'The Who', 'title': '005'})
        self.mpd.mpd_files.append({'artist': 'The The', 'title': '006'})

        self.config = ConfigWrapper()
        return mkapp(self.config, self.mpd, IdleSocket(self.mpd))

    def test_get_artist(self) -> None:
        """Get all files from a certain artist"""
        response = self.fetch('/artist/The%20KLF')
        self.assertEqual(response.code, 200)

        data: dict = loads(response.body)
        tracks = data['tracks']

        self.assertIsInstance(tracks, list)
        self.assertEqual(len(tracks), 3)

        for track in tracks:
            self.assertEqual(track['artist'], 'The KLF')

    def test_get_artist_with_no_files(self) -> None:
        """Get all files from an artist that has no files. Should be empty."""
        response = self.fetch('/artists/Eels')
        self.assertEqual(response.code, 404)


class TestGenreHandler(AsyncHTTPTestCase):
    """
    Test the GenreHandler

    The genre handler searches MPD for songs from a certain genre and returns
    these songs.

    It should not choke on requests with invalid genres.
    """
    def get_app(self) -> Application:
        # Required override for AsyncHTTPTestCase, sets up a dummy
        # webserver for this test.
        self.mpd = MockMPD()
        self.mpd.mpd_files.append({'genre': 'Electro', 'title': '001'})
        self.mpd.mpd_files.append({'genre': 'Electro', 'title': '002'})
        self.mpd.mpd_files.append({'genre': 'Electro', 'title': '003'})
        self.mpd.mpd_files.append({'genre': 'Jazz', 'title': '004'})
        self.mpd.mpd_files.append({'genre': 'Jazz', 'title': '005'})
        self.mpd.mpd_files.append({'genre': 'Pop', 'title': '006'})

        self.config = ConfigWrapper()
        return mkapp(self.config, self.mpd, IdleSocket(self.mpd))

    def test_get_genre(self) -> None:
        """Get all files from a certain genre"""
        response = self.fetch('/genre/Jazz')
        self.assertEqual(response.code, 200)

        data: dict = loads(response.body)
        tracks: list[dict] = data['tracks']

        self.assertIsInstance(tracks, list)
        self.assertEqual(len(tracks), 2)

        for track in tracks:
            self.assertEqual(track['genre'], 'Jazz')

    def test_get_genre_with_no_files(self) -> None:
        """Get all files from a genre that has no files. Should be empty."""
        response = self.fetch('/genre/Rap')
        self.assertEqual(response.code, 200)

        data: dict = loads(response.body)
        tracks = data['tracks']

        self.assertIsInstance(tracks, list)
        self.assertEqual(len(tracks), 0)


class TestCSSHandler(AsyncHTTPTestCase):
    """
    Test the CSSHandler

    The CSS handler serves (static) CSS files from the package resources.

    It should return the CSS file if it's there, or a 404 error otherwise.
    """
    def get_app(self) -> Application:
        # Required override for AsyncHTTPTestCase, sets up a dummy
        # webserver for this test.
        self.mpd = MockMPD()
        self.config = ConfigWrapper()
        return mkapp(self.config, self.mpd, IdleSocket(self.mpd))

    def test_get_css(self) -> None:
        """Get a CSS file"""
        response = self.fetch('/css/fookebox.css')
        self.assertEqual(response.code, 200)
        self.assertEqual(response.body[:4], b'body')

    def test_get_invalid_css(self) -> None:
        """Raise a 404 error if the CSS file cannot be found"""
        response = self.fetch('/css/no-such-file.css')
        self.assertEqual(response.code, 404)


class TestFontHandler(AsyncHTTPTestCase):
    """
    Test the FontHandler

    The font handler serves (static) font files from the package resources.

    It should return the font if it's there, or a 404 error otherwise.
    """
    def get_app(self) -> Application:
        # Required override for AsyncHTTPTestCase, sets up a dummy
        # webserver for this test.
        self.mpd = MockMPD()
        self.config = ConfigWrapper()
        return mkapp(self.config, self.mpd, IdleSocket(self.mpd))

    def test_get_svg_font(self) -> None:
        """Get a font file"""
        response = self.fetch('/fonts/glyphicons-halflings-regular.svg')
        self.assertEqual(response.code, 200)
        self.assertEqual(response.headers['Content-Type'], 'image/svg+xml')
        self.assertEqual(response.body[:5], b'<?xml')

    def test_get_binary_font(self) -> None:
        """Get a font file"""
        response = self.fetch('/fonts/glyphicons-halflings-regular.ttf')
        self.assertEqual(response.code, 200)
        self.assertEqual(response.headers['Content-Type'], 'font/sfnt')

        checksum = md5(response.body).hexdigest()
        self.assertEqual(checksum, 'e18bbf611f2a2e43afc071aa2f4e1512')

    def test_get_invalid_font(self) -> None:
        """Raise a 404 error if the font cannot be found"""
        response = self.fetch('/fonts/no-such-file.ttf')
        self.assertEqual(response.code, 404)


class TestJSHandler(AsyncHTTPTestCase):
    """
    Test the JSHandler

    The JS handler serves (static) JavaScript files from the package resources.

    It should return the script file if it's there, or a 404 error otherwise.
    """
    def get_app(self) -> Application:
        # Required override for AsyncHTTPTestCase, sets up a dummy
        # webserver for this test.
        self.mpd = MockMPD()
        self.config = ConfigWrapper()
        return mkapp(self.config, self.mpd, IdleSocket(self.mpd))

    def test_get_js(self) -> None:
        """Get a font file"""
        response = self.fetch('/js/fookebox.js')
        self.assertEqual(response.code, 200)
        self.assertEqual(response.headers['Content-Type'], 'text/javascript')
        self.assertEqual(response.body[:12], b'"use strict"')

    def test_get_invalid_js(self) -> None:
        """Raise a 404 error if the font cannot be found"""
        response = self.fetch('/js/no-such-file.js')
        self.assertEqual(response.code, 404)


class TestIndexHandler(AsyncHTTPTestCase):
    """
    Test the IndexHandler

    The index handler is responsible for loading the HTML tempalte, filling in
    the artists and genres and loading the appropriate language.
    """
    def get_app(self) -> Application:
        # Required override for AsyncHTTPTestCase, sets up a dummy
        # webserver for this test.
        self.mpd = MockMPD()
        self.mpd.mpd_files.append({'genre': 'Electro', 'artist': 'A01'})
        self.mpd.mpd_files.append({'genre': 'Electro', 'artist': 'A02'})
        self.mpd.mpd_files.append({'genre': 'Electro', 'artist': 'A02'})
        self.mpd.mpd_files.append({'genre': 'Jazz', 'artist': 'A01'})
        self.mpd.mpd_files.append({'genre': 'Jazz', 'artist': 'A03'})
        self.mpd.mpd_files.append({'genre': 'Pop', 'artist': 'A04'})

        self.config = ConfigWrapper()
        return mkapp(self.config, self.mpd, IdleSocket(self.mpd))

    def test_get_index(self) -> None:
        """Load the HTML template"""
        response = self.fetch('/')
        self.assertEqual(response.code, 200)
        self.assertEqual(response.body[:9], b'<!DOCTYPE')

    def test_index_contains_artists_and_genres(self) -> None:
        """Check that the template contains all artists and genres"""
        response = self.fetch('/')
        self.assertEqual(response.code, 200)
        soup = BeautifulSoup(response.body, 'html.parser')

        artists = soup.find_all('li', {'class': 'artist'})
        self.assertEqual(len(artists), 4)

        genres = soup.find_all('li', {'class': 'genre'})
        self.assertEqual(len(genres), 3)

    def test_index_uses_english_language_by_default(self) -> None:
        """If no language has been specified, the page should be in English"""
        response = self.fetch('/')
        self.assertEqual(response.code, 200)
        soup = BeautifulSoup(response.body, 'html.parser')

        artists = soup.find('a', {'id': 'showArtists'})
        self.assertEqual(artists.text, 'Artists')           # type: ignore

    def test_index_uses_german_if_requested(self) -> None:
        """If the browser wants the page in German, we obey"""
        response = self.fetch('/', headers={'Accept-Language': 'de'})
        self.assertEqual(response.code, 200)
        soup = BeautifulSoup(response.body, 'html.parser')

        artists = soup.find('a', {'id': 'showArtists'})
        self.assertEqual(artists.text, 'Künstler')          # type: ignore

    def test_index_falls_back_to_english(self) -> None:
        """If the browser wants the page in Italian, we use English instead"""
        response = self.fetch('/', headers={'Accept-Language': 'it'})
        self.assertEqual(response.code, 200)
        soup = BeautifulSoup(response.body, 'html.parser')

        artists = soup.find('a', {'id': 'showArtists'})
        self.assertEqual(artists.text, 'Artists')           # type: ignore


class TestSocketHandler(AsyncHTTPTestCase):
    """
    Test the SocketHandler

    The socket handler handles web socket connections. It adds new connections
    to the list of connected clients and receives updates from the IdleSocket.
    """
    def get_app(self) -> Application:
        # Required override for AsyncHTTPTestCase, sets up a dummy
        # webserver for this test.
        self.mpd = MockMPD()
        idle = IdleSocket(self.mpd)
        self.clients = idle._clients  # pylint: disable=protected-access
        self.url = f'ws://localhost:{self.get_http_port()}/socket'
        return mkapp(ConfigWrapper(), self.mpd, idle)

    @tornado.testing.gen_test
    def test_open_adds_client_to_clients(self) -> Generator:
        """New connections should be added to the list of clients"""
        self.assertEqual(len(self.clients), 0)

        yield tornado.websocket.websocket_connect(self.url)
        self.assertEqual(len(self.clients), 1)

        yield tornado.websocket.websocket_connect(self.url)
        self.assertEqual(len(self.clients), 2)

        client = self.clients[0]
        self.assertIsInstance(client, SocketHandler)

    @tornado.testing.gen_test
    async def test_close_removes_client_from_clients(self) -> None:
        """Closed connections should be removed from list of clients"""
        self.assertEqual(len(self.clients), 0)

        await tornado.websocket.websocket_connect(self.url)
        ws_client = await tornado.websocket.websocket_connect(self.url)
        await tornado.websocket.websocket_connect(self.url)
        self.assertEqual(len(self.clients), 3)

        ws_client.close()
        await tornado.gen.sleep(.1)
        self.assertEqual(len(self.clients), 2)

    @tornado.testing.gen_test
    def test_receive_update_from_idlesocket(self) -> Generator:
        """Messages to the update function should be forwarded to clients"""
        ws_client = yield tornado.websocket.websocket_connect(self.url)

        for client in self.clients:
            yield client.update({'foo': ['hello']})

        msg = yield ws_client.read_message()
        data = loads(msg)
        self.assertEqual(data, {'foo': ['hello']})
