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
This is the main file for fookebox. It provides the 'main()' entry point as
well as a bunch of helper functions.
"""

import asyncio
import os.path
import sys

from argparse import ArgumentParser, Namespace

import fookebox
from .autoqueue import AutoQueuer
from .config import load_config, default_config
from .mpd import IdleSocket, MPDContext
from .tasks import run_auto_queuer, run_idle
from .util import mkapp


def _parse_args() -> Namespace:
    parser = ArgumentParser(description='Jukebox server')
    parser.add_argument('-c', '--config', required=False,
                        help='configuration file')
    parser.add_argument('--version', action='version',
                        version=f'fookebox { fookebox.__version__ }',
                        help='show version information')
    return parser.parse_args()


async def main() -> None:
    """
    This is the main function. It parses the command line arguments, loads the
    config file and starts the application.
    """
    args = _parse_args()

    if args.config:
        if not os.path.exists(args.config):
            print(f'{args.config} not found', file=sys.stderr)
            sys.exit(1)
        cfg = load_config(args.config)
    else:
        cfg = default_config()

    idle_mpd = MPDContext(cfg.get('mpd_host'), cfg.getint('mpd_port'))
    idle_socket = IdleSocket(idle_mpd)
    run_idle(idle_socket)

    main_mpd = MPDContext(cfg.get('mpd_host'), cfg.getint('mpd_port'))
    if cfg.getboolean('auto_queue'):
        auto_queue_at = cfg.getint('auto_queue_time_left')
        queuer = AutoQueuer(main_mpd, auto_queue_at)
        idle_socket.subscribe(queuer)
        run_auto_queuer(queuer)

    app = mkapp(cfg, main_mpd, idle_socket)
    port = cfg.getint('listen_port')
    print(f'Listening on http://localhost:{port}/')
    app.listen(port)
    await asyncio.Event().wait()


if __name__ == 'fookebox.fookebox':
    asyncio.run(main())
