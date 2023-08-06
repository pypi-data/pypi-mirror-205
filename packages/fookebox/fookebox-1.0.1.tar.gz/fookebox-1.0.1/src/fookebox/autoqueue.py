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
The AutoQueuer is an optional feature that automatically picks songs to play
if the queue runs empty.
"""

import random
import time

from mpd.asyncio import MPDClient
from .mpd import MPD_CMD_PLAYLISTINFO, MPD_CMD_STATUS, MPD_STATE_PAUSE
from .mpd import MPDContext, MPDSubscriber


AUTOQUEUE_MAX_HISTORY_PERCENT = 10


class AutoQueuer(MPDSubscriber):
    """
    A class to automatically pick songs to play if the queue runs empty.

    Methods
    -------
    auto_queue():
        Checks whether a new songs needs to be added to the queue and, if so,
        picks one, adds it and issues a 'play' command.
    update(message):
        Receives an update message from MPD
    """

    # pylint: disable=too-many-instance-attributes
    def __init__(self, mpd: MPDContext, auto_queue_at: int, *,
                 genre: str = '', playlist: str = ''):
        """
        Constructs all the necessary attributes for the AutoQueuer object

        Parameters
        ----------
        mpd : MPDContext
            MPDContext instance to use to connect to MPD
        auto_queue_at : int
            if the remaining time falls below this value, we add a new song
        genre : str, optional
            if this is set, limit automatically picked songs to this genre
        playlist: str, optional
            if this is set, pick the next song from this playlist
        """
        self._mpd = mpd
        self._auto_queue_at = auto_queue_at
        self._genre = genre
        self._playlist = playlist
        self._history: list[str] = []
        self._playlist_offset = 0
        self._mpd_status: dict = {}
        self._ends: float = 0.0
        self._playlist_length: int = 0

    def _queue_length(self) -> int:
        song = int(self._mpd_status.get('song', 0))
        return self._playlist_length - song - 1

    def _requires_new_file(self) -> bool:
        # do nothing in case we haven't seen a status update yet
        if len(self._mpd_status) < 1:
            return False

        # do nothing if MPD is paused
        if self._mpd_status.get('state') == MPD_STATE_PAUSE:
            return False

        # check if there is more in the queue
        if self._queue_length() > 0:
            return False

        now = time.monotonic()
        timeleft = self._ends - now
        return timeleft <= self._auto_queue_at

    def _trim_history(self, keep_n: int) -> None:
        # trim history to keep_n elements
        maxlen = round(keep_n / AUTOQUEUE_MAX_HISTORY_PERCENT)
        self._history = self._history[-maxlen:]

    async def _auto_queue_random(self, client: MPDClient,
                                 entries: list[dict[str, str]]) -> None:
        files = [row['file'] for row in entries if 'file' in row]
        valid = [file for file in files if file not in self._history]

        # if no valid files are left, consider *all* files valid
        if len(valid) < 1:
            valid = files

        if len(valid) > 0:
            file = random.choice(valid)
            self._history.append(file)
            self._trim_history(len(files))
            await client.add(file)

    async def _auto_queue_any(self, client: MPDClient) -> None:
        entries = await client.listall()
        await self._auto_queue_random(client, entries)

    async def _auto_queue_genre(self, client: MPDClient) -> None:
        entries = await client.find('genre', self._genre)
        await self._auto_queue_random(client, entries)

    async def _auto_queue_playlist(self, client: MPDClient) -> None:
        entries = await client.listplaylist(self._playlist)

        # the playlist has shrunk, start from scratch
        if len(entries) <= self._playlist_offset:
            self._playlist_offset = 0

        if len(entries) > self._playlist_offset:
            await client.add(entries[self._playlist_offset])
            self._playlist_offset = (self._playlist_offset + 1) % len(entries)

    async def auto_queue(self) -> None:
        """
        Automatically select a song to be added to the queue.

        - If we are configured to play a specific genre, pick a song from
          that genre.
        - If we are configured to choose from a particular playlist, pick the
          next unplayed song from that playlist.
        - Otherwise, pick a random song from the MPD library that has not been
          played for a while.
        """
        async with self._mpd as client:
            if self._requires_new_file():
                if self._genre:
                    await self._auto_queue_genre(client)
                elif self._playlist:
                    await self._auto_queue_playlist(client)
                else:
                    await self._auto_queue_any(client)
                await client.play()

    async def update(self, message: dict) -> None:
        if MPD_CMD_PLAYLISTINFO in message:
            self._playlist_length = len(message[MPD_CMD_PLAYLISTINFO])
        if MPD_CMD_STATUS in message:
            self._mpd_status = message[MPD_CMD_STATUS]
            now = time.monotonic()
            duration = float(self._mpd_status.get('duration', 0))
            elapsed = float(self._mpd_status.get('elapsed', 0))
            self._ends = now + duration - elapsed
