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
This is our interface to the python-mpd2 library.
"""

from abc import ABC, abstractmethod
from asyncio import Lock, create_task

from mpd.asyncio import MPDClient


MPD_IDLE_PLAYER = 'player'
MPD_IDLE_PLAYLIST = 'playlist'

MPD_CMD_PLAYLISTINFO = 'playlistinfo'
MPD_CMD_STATUS = 'status'

MPD_STATE_PAUSE = 'pause'


class MPDContext:
    """
    The MPDContext class is a context manager that connects to MPD. It can be
    used like this:

      mpd = MPDContext('localhost', 6600)
      with mpd as client:
          print(client.status())

    """
    def __init__(self, host: str, port: int, password: str = ''):
        """
        Constructs all the necessary attributes for the MPDContext object

        Parameters
        ----------
        host : str
            MPD host to connect to
        port : int
            MPD port to connect to
        password : str, optional
            MPD passwort, if required
        """
        self._host = host
        self._port = port
        self._password = password
        self._client = MPDClient()
        self._lock = Lock()

    async def _connect(self) -> None:
        await self._client.connect(self._host, self._port)
        await self._client.consume(1)           # pylint: disable=no-member

        if self._password:
            await self._client.password(self._password) \
                                                # pylint: disable=no-member

    async def __aenter__(self) -> MPDClient:
        await self._lock.acquire()
        try:
            await self._connect()
        except Exception as exc:
            self._lock.release()
            raise exc

        return self._client

    async def __aexit__(self, *args: list) -> None:
        self._client.disconnect()
        self._lock.release()


class MPDSubscriber(ABC):
    # pylint: disable=too-few-public-methods
    """
    An abstract class that defines an interface for listeners interested in
    status updates from MPD through the IdleSocket.
    """
    @abstractmethod
    async def update(self, message: dict) -> None:
        """Receive a status update from MPD"""


class IdleSocket:
    # pylint: disable=too-few-public-methods
    """
    The IdleSocket connects to MPD, listens for events in Idle mode and
    forwards these events to connected clients.
    """
    def __init__(self, mpd: MPDContext):
        """
        Constructs all the necessary attributes for the IdleSocket object

        Parameters
        ----------
        mpd : MPDContext
            Client object to access MPD
        """
        self._mpd = mpd
        self._clients: list[MPDSubscriber] = []
        self._cache: dict = {}

    async def _notify(self, message: dict) -> None:
        for client in self._clients:
            await client.update(message)

    async def _update(self, mpd: MPDClient, events: list[str]) -> None:
        update = {}

        if MPD_IDLE_PLAYER in events:
            update[MPD_CMD_STATUS] = await mpd.status()
        if MPD_IDLE_PLAYLIST in events:
            update[MPD_CMD_PLAYLISTINFO] = await mpd.playlistinfo()

        self._cache.update(update)
        await self._notify(update)

    async def _idle(self, mpd: MPDClient) -> None:
        async for events in mpd.idle():
            await self._update(mpd, events)

    def subscribe(self, client: MPDSubscriber) -> None:
        """Subscribe client to MPD updates

        Parameters
        ----------
        client : MPDSubscriber
            Client object to subscribe. The client will immediately get a
            cached copy of the last known MPD state and will receive status
            updates as they tickle in.
        """
        if self._cache:
            create_task(client.update(self._cache))

        self._clients.append(client)

    def unsubscribe(self, client: MPDSubscriber) -> None:
        """Unsubscribe client from MPD updates

        Parameters
        ----------
        client : MPDSubscriber
            Client to unsubscribe. The client will no longer get staus updates.
        """
        self._clients.remove(client)

    async def listen(self) -> None:
        """Open MPD connection and wait for events"""
        async with self._mpd as mpd:
            await self._update(mpd, [MPD_IDLE_PLAYLIST, MPD_IDLE_PLAYER])
            await self._idle(mpd)
