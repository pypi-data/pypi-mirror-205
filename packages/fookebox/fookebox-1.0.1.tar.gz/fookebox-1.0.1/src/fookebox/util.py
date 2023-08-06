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
"""This module contains various helper functions for fookebox"""

from importlib import resources
from typing import Any

from tornado import locale
from tornado.web import Application

import fookebox
from .handlers import ArtistHandler, ControlHandler, CoverArtHandler
from .handlers import CSSHandler, FontHandler, GenreHandler, IndexHandler
from .handlers import JSHandler, QueueHandler, SocketHandler
from .mpd import IdleSocket, MPDContext


def mkapp(cfg: Any, mpd: MPDContext,
          idle: IdleSocket) -> Application:
    """Creates a Tornado application

    Parameters
    ----------
    cfg : SectionProxy
        A configparser.SectionProxy object with the fookebox configuration
    mpd : MPDContext
        MPDContext instance to use to connect to MPD
    idle : IdleSocket
        A IdleSocket object from which we wish to receive status updates
    """
    res = resources.files(fookebox).joinpath('i18n')
    with resources.as_file(res) as dir_:
        locale.load_gettext_translations(str(dir_), domain='fookebox')
    locale.set_default_locale('en')

    return Application([
        (r'/', IndexHandler,
            {'mpd': mpd, 'cfg': cfg}),
        (r'/css/(.*)', CSSHandler),
        (r'/js/(.*)', JSHandler),
        (r'/fonts/(.*)', FontHandler),
        (r'/artist/(.*)', ArtistHandler,
            {'mpd': mpd}),
        (r'/genre/(.*)', GenreHandler,
            {'mpd': mpd}),
        (r'/queue/(\d+)', QueueHandler,
            {'mpd': mpd, 'cfg': cfg}),
        (r'/queue', QueueHandler,
            {'mpd': mpd, 'cfg': cfg}),
        (r'/control', ControlHandler,
            {'mpd': mpd, 'cfg': cfg}),
        (r'/cover/(.*)', CoverArtHandler,
            {'mpd': mpd, 'cfg': cfg}),
        ('/socket', SocketHandler,
            {'idle': idle})
    ])
