# fookebox, https://code.ott.net/fookebox/
# Copyright (c) 2007-2023 Stefan Ott. all rights reserved.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, version 3.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""
This module contains all of fookbox's RequestHandlers.
"""

from configparser import SectionProxy
from importlib import resources
import json

import magic
from mpd.base import CommandError
from tornado import template
from tornado.web import HTTPError, RequestHandler
from tornado.websocket import WebSocketHandler

import fookebox
from .mpd import IdleSocket, MPDContext, MPDSubscriber


class ArtistHandler(RequestHandler):
    """
    A RequestHandler to load tracks by a particular artist.

    Methods
    -------
    get(artist):
        Load tracks of by particular artist.
    """
    # pylint: disable=abstract-method
    def initialize(self, mpd: MPDContext) -> None:
        """Initialize the ArtistHandler object"""
        # pylint: disable=attribute-defined-outside-init
        self._mpd = mpd

    async def get(self, artist: str) -> None:
        """
        Returns tracks by a particular artist.

        Parameters
        ----------
        artist : str
            name of the artist

        Returns
        -------
        A list of tracks by the specified artist, wrapped in a dictionary under
        the 'tracks' key.
        """
        async with self._mpd as client:
            hits = await client.find('artist', artist)

        self.write({'tracks': hits})


class GenreHandler(RequestHandler):
    """
    A RequestHandler to load tracks of a particular genre.

    Methods
    -------
    get(genre):
        Load tracks of a particular genre.
    """
    # pylint: disable=abstract-method
    def initialize(self, mpd: MPDContext) -> None:
        """Initialize the GenreHandler object"""
        # pylint: disable=attribute-defined-outside-init
        self._mpd = mpd

    async def get(self, genre: str) -> None:
        """
        Returns tracks from a particular genre.

        Parameters
        ----------
        genre : str
            name of the genre

        Returns
        -------
        A list of tracks from the specified genre, wrapped in a dictionary
        under the 'tracks' key.
        """
        async with self._mpd as client:
            hits = await client.find('genre', genre)

        self.write({'tracks': hits})


class ControlHandler(RequestHandler):
    """
    A RequestHandler to control MPD.

    This handler allows clients to send commands such as play, pause etc. to
    MPD.

    Methods
    -------
    post():
        Send a command to MPD
    """
    # pylint: disable=abstract-method
    def initialize(self, mpd: MPDContext, cfg: SectionProxy) -> None:
        """Initialize the ControlHandler object"""
        # pylint: disable=attribute-defined-outside-init
        self._mpd = mpd
        self._cfg = cfg

    async def post(self) -> None:
        """
        Send a command to MPD

        A JSON-encoded dictionary with the keyword 'action' and the MPD command
        as a value is expected in the POST body. Something like this:

            {'action': 'play'}

        Valid commands are play, pause, next, prev, volup, voldown and rebuild.

        Whether or not clients are allowed to send MPD commands can be
        configured using the 'enable_controls' config option.

        Exceptions
        ----------
        - If controls have been disabled, a HTTP 403 error is raised.
        - If the supplied JSON data is invalid, a HTTP 400 error is raised.
        - If an unknown command has been sent, a HTTP 400 error is raised.
        """
        if not self._cfg.getboolean('enable_controls'):
            raise HTTPError(403, 'Controls disabled')

        try:
            data = json.loads(self.request.body)
        except json.decoder.JSONDecodeError as exc:
            raise HTTPError(400, 'Invalid JSON data') from exc

        commands = {
            'next': lambda client: client.next(),
            'prev': lambda client: client.previous(),
            'play': lambda client: client.play(),
            'pause': lambda client: client.pause(),
            'volup': lambda client: client.volume(+10),
            'voldown': lambda client: client.volume(-10),
            'rebuild': lambda client: client.update()
        }

        if (action := data.get('action')) in commands:
            async with self._mpd as client:
                await commands[action](client)
        else:
            raise HTTPError(400, 'Invalid command')


class CoverArtHandler(RequestHandler):
    """
    A RequestHandler that serves cover art.

    Methods
    -------
    get(filename):
        Get cover art for a file
    """
    # pylint: disable=abstract-method
    def initialize(self, mpd: MPDContext, cfg: SectionProxy) -> None:
        """Initialize the CoverArtHandler object"""
        # pylint: disable=attribute-defined-outside-init
        self._mpd = mpd
        self._cfg = cfg

    async def get(self, filename: str) -> None:
        """
        Returns cover art for a particular file.

        Parameters
        ----------
        filename : str
            name of the file

        Exceptions
        ----------
        If no cover art is found, a HTTP 404 error is raised
        """
        async with self._mpd as client:
            try:
                albumart = await client.albumart(filename)
            except CommandError as exc:
                raise HTTPError(404, 'Cover art not found') from exc

        data = albumart['binary']
        mime = magic.from_buffer(data, mime=True)

        self.write(data)
        self.set_header('content-type', mime)


def _read_resource(dir_: str, filename: str) -> str:
    src = resources.files(fookebox).joinpath(dir_).joinpath(filename)
    with resources.as_file(src) as path:
        with open(path, 'r', encoding='utf-8') as file:
            return file.read()


def _read_binary_resource(dir_: str, filename: str) -> bytes:
    src = resources.files(fookebox).joinpath(dir_).joinpath(filename)
    with resources.as_file(src) as path:
        with open(path, 'rb') as file:
            return file.read()


class CSSHandler(RequestHandler):
    """A RequestHandler that serves CSS files from the package resources."""
    # pylint: disable=abstract-method
    def get(self, filename: str) -> None:
        """
        Get the a CSS file from the package resources.

        Parameters
        ----------
        filename : str
            name of the file
        """
        try:
            data = _read_resource('css', filename)
        except FileNotFoundError as exc:
            raise HTTPError(404) from exc

        self.set_header('content-type', 'text/css')
        self.write(data)


class FontHandler(RequestHandler):
    """A RequestHandler that serves fonts from the package resources."""
    # pylint: disable=abstract-method
    def get(self, filename: str) -> None:
        """
        Get the a font from the package resources.

        Parameters
        ----------
        filename : str
            name of the font file
        """
        try:
            data = _read_binary_resource('fonts', filename)
        except FileNotFoundError as exc:
            raise HTTPError(404) from exc

        mime = magic.from_buffer(data, mime=True)

        self.write(data)
        self.set_header('content-type', mime)


class IndexHandler(RequestHandler):
    """A RequestHandler that serves the index HTML file."""
    # pylint: disable=abstract-method
    def initialize(self, mpd: MPDContext, cfg: SectionProxy) -> None:
        """Initialize the IndexHandler object"""
        # pylint: disable=attribute-defined-outside-init
        self.mpd = mpd
        self.cfg = cfg

    async def get(self) -> None:
        """
        Load the index HTML file.

        The HTML file comes pre-loaded with all available artists and genres,
        rendered in the browser's preferred language (if available).
        """
        async with self.mpd as client:
            artists = [x['artist'] for x in await client.list('artist')]
            genres = [x['genre'] for x in await client.list('genre')]

        markup = _read_resource('templates', 'client.html')
        tpl = template.Template(markup)
        output = tpl.generate(config=self.cfg, artists=artists, genres=genres,
                              locale=self.get_browser_locale())
        self.write(output)


class JSHandler(RequestHandler):
    """A RequestHandler that serves JavaScript from the package resources."""
    # pylint: disable=abstract-method
    def get(self, filename: str) -> None:
        """
        Get the a JavaScript file from the package resources.

        Parameters
        ----------
        filename : str
            name of the file
        """
        try:
            data = _read_resource('js', filename)
        except FileNotFoundError as exc:
            raise HTTPError(404) from exc

        self.set_header('content-type', 'text/javascript')
        self.write(data)


class QueueHandler(RequestHandler):
    # pylint: disable=abstract-method
    """
    A RequestHandler that allows clients to interact with MPD's queue.

    Methods
    -------
    post():
        Add an arbitrary number of tracks to the queue
    delete():
        Remove a track from the queue
    """
    def initialize(self, mpd: MPDContext, cfg: SectionProxy) -> None:
        # pylint: disable=attribute-defined-outside-init
        """Initialize the QueueHandler object"""
        self._mpd = mpd
        self._cfg = cfg

    async def post(self) -> None:
        """
        Add tracks to the queue.

        A JSON-encoded list of tracks to be added to the queue is read from the
        POST body. The tracks are then added, one by one, to the queue until
        there are no more tracks left or the queue is full.

        The queue size is determined from the max_queue_length configuration
        option.

        Exceptions
        ----------
        - If the queue limit has been exceeded, a HTTP 409 error is raised.
        - If the supplied JSON data is invalid, a HTTP 400 error is raised.
        """
        try:
            data = json.loads(self.request.body)
        except json.decoder.JSONDecodeError as exc:
            raise HTTPError(400, 'Invalid JSON data') from exc

        dir_ = data.get('files', [])
        maxlen = self._cfg.getint('max_queue_length')

        if not isinstance(dir_, list):
            raise HTTPError(400, 'Invalid data')

        async with self._mpd as client:
            for file in dir_:
                playlist = list(await client.playlist())[1:]
                if len(playlist) >= maxlen:
                    raise HTTPError(409, 'Queue full')
                await client.add(file)

            await client.play()

    async def delete(self, position: str) -> None:
        """
        Remove a track from the queue.

        The queue position of the track to be removed is expected to be passed
        in the URL.

        Removing tracks from the queue can be allowed / disallowed using the
        'enable_song_removal' configuration option.

        Parameters
        ----------
        position : int
            position in the queue to remove

        Exceptions
        ----------
        - If removing items from the queue has been disabled, a HTTP 403 error
          is raised.
        - If the supplied position is not valid, a HTTP 400 error is raised.
        """
        if not self._cfg.get('enable_song_removal'):
            raise HTTPError(403)

        async with self._mpd as client:
            try:
                await client.delete(int(position))
            except CommandError as exc:
                raise HTTPError(400, str(exc)) from exc


class SocketHandler(WebSocketHandler, MPDSubscriber):
    # pylint: disable=abstract-method
    """
    A WebSocketHandler for clients that wish to receive status updates.
    """
    def initialize(self, idle: IdleSocket) -> None:
        # pylint: disable=attribute-defined-outside-init
        """Initialize the SocketHandler object"""
        self._idle = idle

    def open(self, *args: str, **kwargs: str) -> None:
        self._idle.subscribe(self)

    def on_close(self) -> None:
        self._idle.unsubscribe(self)

    async def update(self, message: dict) -> None:
        self.write_message(json.dumps(message))
