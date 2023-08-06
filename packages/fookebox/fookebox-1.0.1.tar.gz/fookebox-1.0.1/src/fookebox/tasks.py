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

"""Background tasks for fookebox"""

import asyncio

from .mpd import IdleSocket
from .autoqueue import AutoQueuer


# References to background tasks. This is to prevent the tasks from being
# garbage-collected mid-execution, as recommended on
# https://docs.python.org/3/library/asyncio-task.html#asyncio.create_task
_background_tasks = set()


def run_auto_queuer(queuer: AutoQueuer) -> None:
    """
    Run the auto-queue task.

    If the AutoQueuer exits due to an unexptected problem, keep restarting it.

    Parameters
    ----------
    queuer : AutoQueuer
        AutoQueuer object to use for the task
    """
    async def auto_queue_restart() -> None:
        await asyncio.sleep(1)
        run_auto_queuer(queuer)

    def auto_queuer_done(task: asyncio.Task) -> None:
        _background_tasks.discard(task)

        if task.cancelled():
            return

        if (exc := task.exception()):
            print(exc)

        asyncio.create_task(auto_queue_restart())

    task = asyncio.create_task(queuer.auto_queue())
    task.add_done_callback(auto_queuer_done)
    _background_tasks.add(task)


def run_idle(socket: IdleSocket) -> None:
    """
    Run the idle task: Connect to MPD and start forwarding messages.

    If the IdleSocket exits due to an unexptected problem, keep restarting it.

    Parameters
    ----------
    socket : IdleSocket
        IdleSocket object to use for the MPD connection
    """
    async def idle_restart() -> None:
        await asyncio.sleep(1)
        run_idle(socket)

    async def idle_task() -> None:
        await socket.listen()

    def idle_done(task: asyncio.Task) -> None:
        _background_tasks.discard(task)

        if task.cancelled():
            return

        print(task.exception())
        asyncio.create_task(idle_restart())

    task = asyncio.create_task(idle_task())
    task.add_done_callback(idle_done)
    _background_tasks.add(task)
