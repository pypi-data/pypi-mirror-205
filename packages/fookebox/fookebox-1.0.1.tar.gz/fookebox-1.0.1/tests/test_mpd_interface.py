"""
Test the MPD interface classes
"""
from asyncio import all_tasks, sleep, wait_for
from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock, patch
import asyncio.exceptions

from mpd.asyncio import MPDClient

from fookebox.mpd import IdleSocket, MPDSubscriber, MPDContext
from tests.common import MockMPD, all_tasks_done_except


class MockSubscriber(MPDSubscriber):
    """Mock class for MPDSubscriber which simply logs all messages received"""
    # pylint: disable=too-few-public-methods
    def __init__(self) -> None:
        self.msg: list[dict] = []

    async def update(self, message: dict) -> None:
        self.msg.append(message)


class TestIdleSocket(IsolatedAsyncioTestCase):
    """
    Test the auto-queue mechanism.

    The auto-queuer should check the current state to figure out whether a new
    song should be added to the queue.
    """
    def setUp(self) -> None:
        self.mpd = MockMPD()
        self.sock = IdleSocket(self.mpd)

    async def test_cache_is_sent_to_new_subscribers(self) -> None:
        """New subscribers should receive a full cache dump"""
        # pylint: disable=protected-access
        self.sock._cache = {'status': {'volume': '28'}, 'foo': 'bar'}
        orig_tasks = all_tasks()

        sub = MockSubscriber()
        self.sock.subscribe(sub)

        await all_tasks_done_except(orig_tasks)
        self.assertEqual(sub.msg, [{'status': {'volume': '28'}, 'foo': 'bar'}])

    async def test_subscribers_get_messages_on_startup(self) -> None:
        """All subscribers should get update messages on startup"""
        subs = [MockSubscriber(), MockSubscriber(), MockSubscriber()]
        for sub in subs:
            self.sock.subscribe(sub)

        self.mpd.mpd_status = {'volume': '50'}
        self.mpd.mpd_queue = ['001.mp3']
        await self.sock.listen()

        self.assertEqual(len(subs), 3)
        self.assertEqual(len(subs[0].msg), 1)
        self.assertEqual(len(subs[1].msg), 1)
        self.assertEqual(len(subs[2].msg), 1)

        self.assertEqual(subs[0].msg[0],
                         {'status': {'volume': '50'},
                          'playlistinfo': [{'file': '001.mp3'}]})

    async def test_subscribers_get_status_update(self) -> None:
        """All subscribers should get status updates when available"""
        self.mpd.mpd_status = {'volume': '50'}
        self.mpd.mpd_queue = ['001.mp3']

        await self.sock._idle(self.mpd)  # pylint: disable=protected-access

        sub = MockSubscriber()
        self.sock.subscribe(sub)

        await sleep(.1)
        self.assertEqual(len(sub.msg), 0)

        await self.mpd.idle_queue.put(['player'])
        await self.sock._idle(self.mpd)  # pylint: disable=protected-access
        self.assertEqual(sub.msg, [{'status': {'volume': '50'}}])

    async def test_subscribers_get_playlists_update(self) -> None:
        """All subscribers should get playlist updates when available"""
        self.mpd.mpd_status = {'volume': '50'}
        self.mpd.mpd_queue = ['001.mp3']

        await self.sock._idle(self.mpd)  # pylint: disable=protected-access

        sub = MockSubscriber()
        self.sock.subscribe(sub)

        await sleep(.1)
        self.assertEqual(len(sub.msg), 0)

        await self.mpd.idle_queue.put(['playlist'])
        await self.sock._idle(self.mpd)  # pylint: disable=protected-access
        self.assertEqual(sub.msg, [{'playlistinfo': [{'file': '001.mp3'}]}])

    async def test_subscribers_get_playlists_and_status_update(self) -> None:
        """All subscribers should get combined status and playlist updates"""
        self.mpd.mpd_status = {'volume': '50'}
        self.mpd.mpd_queue = ['001.mp3']

        await self.sock._idle(self.mpd)  # pylint: disable=protected-access

        sub = MockSubscriber()
        self.sock.subscribe(sub)

        await sleep(.1)
        self.assertEqual(len(sub.msg), 0)

        await self.mpd.idle_queue.put(['playlist', 'player'])
        await self.sock._idle(self.mpd)  # pylint: disable=protected-access
        self.assertEqual(sub.msg, [{'playlistinfo': [{'file': '001.mp3'}],
                                    'status': {'volume': '50'}}])


async def _get(mpd: MPDContext) -> None:
    async with mpd:
        pass


class TestMPDContext(IsolatedAsyncioTestCase):
    """
    Test the MPDContext class

    MPDContext is a wrapper around python-mpd2 that connects to MPD when needed
    and makes sure that only one client ever talks to MPD at the same time.
    """
    @patch.object(MPDContext, '_connect', side_effect=OSError)
    async def test_connection_error(self, _: None) -> None:
        """Make sure that connection errors are passed on to clients"""
        mpd = MPDContext('', 0)
        with self.assertRaises(OSError):
            async with mpd:
                pass

    @patch.object(MPDContext, '_connect', side_effect=OSError)
    async def test_release_lock_on_connection_error(self, _: None) -> None:
        """Make sure that the lock is released if the connection fails"""
        mpd = MPDContext('', 0)
        with self.assertRaises(OSError):
            async with mpd:
                pass

        # if the lock is not released in the first call, this call will never
        # complete
        with self.assertRaises(OSError):
            async with mpd:
                pass

    @patch.object(MPDContext, '_connect')
    async def test_aenter_returns_client(self, _: None) -> None:
        """Make sure that we get a client object when entering the context"""
        mpd = MPDContext('', 0)
        async with mpd as client:
            self.assertTrue(isinstance(client, MPDClient))

    @patch.object(MPDContext, '_connect')
    async def test_lock(self, _: None) -> None:
        """Make sure that only one client can use the socket at any time"""
        mpd = MPDContext('', 0)
        async with mpd:
            with self.assertRaises(asyncio.exceptions.TimeoutError):
                await wait_for(_get(mpd), timeout=0.1)


class TestMPDContextConnection(IsolatedAsyncioTestCase):
    # pylint: disable=protected-access
    # pylint: disable=no-member
    """
    Test the way to MPDContext class connects to MPD
    """
    def setUp(self) -> None:
        self.mpd = MPDContext('example.org', 1234)
        self.mpd._client = AsyncMock(spec=MPDClient)
        self.mpd._client.attach_mock(AsyncMock(), 'connect')
        self.mpd._client.attach_mock(AsyncMock(), 'consume')
        self.mpd._client.attach_mock(AsyncMock(), 'password')

    async def test_connect_enables_consume(self) -> None:
        """Make sure that we enable 'consume' mode when connecting"""
        async with self.mpd:
            self.mpd._client.consume.assert_called_with(1)

    async def test_connect_without_password(self) -> None:
        """Make sure that the correct hostname and port number are used"""
        async with self.mpd:
            self.mpd._client.connect.assert_called_with('example.org', 1234)
            self.mpd._client.password.assert_not_called()

    async def test_connect_with_password(self) -> None:
        """Make sure that the correct password is used"""
        mpd = MPDContext('example.org', 1234, 's3kr1t')
        self.assertEqual(mpd._password, 's3kr1t')

        mpd._client = AsyncMock(spec=MPDClient)
        mpd._client.attach_mock(AsyncMock(), 'connect')
        mpd._client.attach_mock(AsyncMock(), 'consume')
        mpd._client.attach_mock(AsyncMock(), 'password')

        async with mpd:
            mpd._client.connect.assert_called_with('example.org', 1234)
            mpd._client.password.assert_called_with('s3kr1t')

    async def test_disconnect_on_exit(self) -> None:
        """Make sure that the client connection is closed on exit"""
        async with self.mpd:
            self.mpd._client.connect.assert_called()
            self.mpd._client.disconnect.assert_not_called()
            self.mpd._client.connect.reset_mock()

        self.mpd._client.connect.assert_not_called()
        self.mpd._client.disconnect.assert_called()
