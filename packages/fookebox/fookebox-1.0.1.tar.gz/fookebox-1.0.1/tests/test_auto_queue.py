"""
Test the auto-queue functionality

If enabled, auto-queue should feed the jukebox with new songs to play if the
queue runs empty. It can optionally be fine-tuned by specifying a genre or a
playlist from which to choose the songs.
"""

from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock, patch

from fookebox.autoqueue import AutoQueuer
from tests.common import MockMPD


class TestAutoQueueRequiresNewFile(IsolatedAsyncioTestCase):
    """
    Test the auto-queue mechanism.

    The auto-queuer should check the current state to figure out whether a new
    song should be added to the queue.
    """
    def setUp(self) -> None:
        self.queuer = AutoQueuer(MockMPD(), 5)

    async def test_requires_no_new_file_when_playing(self) -> None:
        """Do not require a new file if there is enough time left"""
        status = {
            'duration': '138.669',
            'elapsed': '48.446'
        }

        await self.queuer.update({'status': status})
        await self.queuer.update({'playlistinfo': [None]})

        # pylint: disable=protected-access
        self.assertFalse(self.queuer._requires_new_file())

    async def test_requires_no_new_file_when_song_is_queued(self) -> None:
        """Do not require a new file if there is something else in the queue"""
        status = {
            'duration': '138.669',
            'elapsed': '138.400'
        }

        await self.queuer.update({'status': status})
        await self.queuer.update({'playlistinfo': [None, None]})

        # pylint: disable=protected-access
        self.assertFalse(self.queuer._requires_new_file())

    async def test_requires_new_file_when_playing_is_almost_over(self) -> None:
        """Require a new file if the current song is almost over"""
        status = {
            'duration': '138.669',
            'elapsed': '135'
        }

        await self.queuer.update({'status': status})
        await self.queuer.update({'playlistinfo': [None]})

        # pylint: disable=protected-access
        self.assertTrue(self.queuer._requires_new_file())

    async def test_req_new_file_when_playing_second(self) -> None:
        """Require a new file if the current, non-first song is almost over"""
        status = {
            'duration': '195.897',
            'elapsed': '194.554',
            'song': '1'
        }
        playlistinfo = [{'file': '001.mp3'}, {'file': '002.mp3'}]

        await self.queuer.update({'status': status})
        await self.queuer.update({'playlistinfo': playlistinfo})

        # pylint: disable=protected-access
        self.assertTrue(self.queuer._requires_new_file())

    async def test_req_no_new_file_when_more_in_queue(self) -> None:
        """Require no new file if the current, non-first song is almost over
           but there is more in the queue"""
        status = {
            'duration': '195.897',
            'elapsed': '194.554',
            'song': '1'
        }
        playlistinfo = [{'file': '1.mp3'}, {'file': '2.mp3'},
                        {'file': '3.mp3'}]

        await self.queuer.update({'status': status})
        await self.queuer.update({'playlistinfo': playlistinfo})

        # pylint: disable=protected-access
        self.assertFalse(self.queuer._requires_new_file())

    async def test_req_no_new_file_if_no_status_seen(self) -> None:
        """Do not require a new file if we have never seen a status update"""
        playlistinfo = [{'file': '1.mp3'}, {'file': '2.mp3'},
                        {'file': '3.mp3'}]

        await self.queuer.update({'playlistinfo': playlistinfo})

        # pylint: disable=protected-access
        self.assertFalse(self.queuer._requires_new_file())

    async def test_req_no_new_file_if_paused(self) -> None:
        """Do not require a new file if the player is paused"""
        status = {
            'duration': '138.669',
            'elapsed': '135',
            'state': 'pause'
        }

        # pylint: disable=protected-access
        await self.queuer.update({'status': status})
        await self.queuer.update({'playlistinfo': [None]})
        self.assertFalse(self.queuer._requires_new_file())

    async def test_req_new_file_if_stopped(self) -> None:
        """Do not require a new file if the player is stopped"""
        status = {
            'duration': '138.669',
            'elapsed': '135',
            'state': 'stop'
        }

        # pylint: disable=protected-access
        await self.queuer.update({'status': status})
        await self.queuer.update({'playlistinfo': [None]})
        self.assertTrue(self.queuer._requires_new_file())


class TestAutoQueueHistory(IsolatedAsyncioTestCase):
    """
    Test the auto-queue history
    """
    def test_trim_history(self) -> None:
        """The AutoQueuer should keep a history of up to 10% of our library"""
        # pylint: disable=protected-access
        queuer = AutoQueuer(MockMPD(), 5)
        queuer._history = list(str(x) for x in range(1000))
        queuer._trim_history(500)
        self.assertEqual(len(queuer._history), 50)
        self.assertEqual(queuer._history[0], '950')
        self.assertEqual(queuer._history[49], '999')

    def test_trim_history_round(self) -> None:
        """The AutoQueuer should round sanely when trimming the history"""
        # pylint: disable=protected-access
        queuer = AutoQueuer(MockMPD(), 5)
        queuer._history = list(str(x) for x in range(1000))
        queuer._trim_history(503)
        self.assertEqual(len(queuer._history), 50)
        self.assertEqual(queuer._history[0], '950')
        self.assertEqual(queuer._history[49], '999')

    def test_trim_short_history(self) -> None:
        """The AutoQueuer should do nothing when trimming a short history"""
        # pylint: disable=protected-access
        queuer = AutoQueuer(MockMPD(), 5)
        queuer._history = list(str(x) for x in range(10))
        queuer._trim_history(500)
        self.assertEqual(len(queuer._history), 10)
        self.assertEqual(queuer._history[0], '0')
        self.assertEqual(queuer._history[9], '9')


class TestAutoQueuePlaylist(IsolatedAsyncioTestCase):
    """
    Test the auto-queue-playlist functionality.

    If a playlist has been specified, auto-queue should pick the next unplayed
    song from that playlist.
    """
    def setUp(self) -> None:
        self.mpd = MockMPD()
        self.mpd.mpd_playlists["test"] = ["01", "02", "03"]
        self.queuer = AutoQueuer(self.mpd, 5)

    @patch.object(AutoQueuer, '_requires_new_file', return_value=True)
    async def test_auto_queue_playlist_starts_playback(self, _: None) -> None:
        """Auto-queue from a playlist should issue a 'play' command"""
        self.assertEqual(self.mpd.commands, [])

        queuer = AutoQueuer(self.mpd, 5, playlist='test101')
        await queuer.auto_queue()
        self.assertEqual(self.mpd.commands, ['play'])

        await queuer.auto_queue()
        self.assertEqual(self.mpd.commands, ['play', 'play'])

    @patch.object(AutoQueuer, '_requires_new_file', return_value=True)
    async def test_auto_queue_use_playlist(self, _: None) -> None:
        """
        If a playlist has been configured, auto-queue should only play songs
        from that playlist.
        """
        # pylint: disable=protected-access
        queuer = AutoQueuer(self.mpd, 5)

        queuer._auto_queue_playlist = AsyncMock()   # type: ignore
        await queuer.auto_queue()
        queuer._auto_queue_playlist.assert_not_called()

        queuer = AutoQueuer(self.mpd, 5, playlist='test101')
        queuer._auto_queue_playlist = AsyncMock()   # type: ignore
        await queuer.auto_queue()
        queuer._auto_queue_playlist.assert_called()

    @patch.object(AutoQueuer, '_requires_new_file', return_value=True)
    async def test_auto_queue_from_playlist_rotate(self, _: None) -> None:
        """Start from scratch once the playlist has been fully played"""
        self.assertEqual(self.mpd.mpd_queue, [])

        queuer = AutoQueuer(self.mpd, 5, playlist='test')
        await queuer.auto_queue()
        self.assertEqual(self.mpd.mpd_queue, ['01'])

        await queuer.auto_queue()
        self.assertEqual(self.mpd.mpd_queue, ['01', '02'])

        await queuer.auto_queue()
        self.assertEqual(self.mpd.mpd_queue, ['01', '02', '03'])

        await queuer.auto_queue()
        self.assertEqual(self.mpd.mpd_queue, ['01', '02', '03', '01'])

        await queuer.auto_queue()
        self.assertEqual(self.mpd.mpd_queue, ['01', '02', '03', '01', '02'])

    @patch.object(AutoQueuer, '_requires_new_file', return_value=True)
    async def test_auto_queue_from_changing_playlist(self, _: None) -> None:
        """Restart from the top if our playlist gets shorter"""
        self.assertEqual(self.mpd.mpd_queue, [])

        queuer = AutoQueuer(self.mpd, 5, playlist='test')
        await queuer.auto_queue()
        self.assertEqual(self.mpd.mpd_queue, ['01'])

        await queuer.auto_queue()
        self.assertEqual(self.mpd.mpd_queue, ['01', '02'])

        self.mpd.mpd_playlists["test"] = ["01"]

        await queuer.auto_queue()
        self.assertEqual(self.mpd.mpd_queue, ['01', '02', '01'])

        await queuer.auto_queue()
        self.assertEqual(self.mpd.mpd_queue, ['01', '02', '01', '01'])

    @patch.object(AutoQueuer, '_requires_new_file', return_value=True)
    async def test_auto_queue_from_empty_playlist(self, _: None) -> None:
        """Auto-queue from empty playlist: Quietly do nothing"""
        self.assertEqual(self.mpd.mpd_queue, [])

        queuer = AutoQueuer(self.mpd, 5, playlist='test1')
        self.mpd.mpd_playlists["test1"] = []
        queuer._playlist = "test1"  # pylint: disable=protected-access

        await queuer.auto_queue()
        self.assertEqual(self.mpd.mpd_queue, [])

        await queuer.auto_queue()
        self.assertEqual(self.mpd.mpd_queue, [])


class TestAutoQueueGenre(IsolatedAsyncioTestCase):
    """
    Test the auto-queue-genre functionality.

    If a genre has been specified, auto-queue should pick any random song from
    the specified genre from mpd and start playing it.
    """
    def setUp(self) -> None:
        self.mpd = MockMPD()
        self.queuer = AutoQueuer(self.mpd, 5)

    @patch.object(AutoQueuer, '_requires_new_file', return_value=True)
    async def test_auto_queue_use_genre_when_configured(self, _: None) -> None:
        """
        If a genre has been configured, auto-queue should only play songs from
        that genre.
        """
        # pylint: disable=protected-access
        queuer = AutoQueuer(self.mpd, 5)
        queuer._auto_queue_genre = AsyncMock()  # type: ignore
        await queuer.auto_queue()
        queuer._auto_queue_genre.assert_not_called()

        queuer = AutoQueuer(self.mpd, 5, genre='House')
        queuer._auto_queue_genre = AsyncMock()  # type: ignore
        await queuer.auto_queue()
        queuer._auto_queue_genre.assert_called()

    @patch.object(AutoQueuer, '_requires_new_file', return_value=True)
    async def test_auto_queue_genre_issue_play_command(self, _: None) -> None:
        """Auto-queue with a genre should issue a 'play' command"""
        self.assertEqual(self.mpd.commands, [])

        queuer = AutoQueuer(self.mpd, 5, genre='House')
        await queuer.auto_queue()
        self.assertEqual(self.mpd.commands, ['play'])

    @patch.object(AutoQueuer, '_requires_new_file', return_value=True)
    async def test_auto_queue_from_genre(self, _: None) -> None:
        """Auto queue any random file from a specific genre"""
        self.mpd.mpd_files.append({"file": "J1", "genre": "Jazz"})
        self.mpd.mpd_files.append({"file": "J2", "genre": "Jazz"})
        self.mpd.mpd_files.append({"file": "J3", "genre": "Jazz"})
        self.mpd.mpd_files.append({"file": "J4", "genre": "Blues"})

        self.assertEqual(self.mpd.mpd_queue, [])

        queuer = AutoQueuer(self.mpd, 5, genre='Jazz')

        for i in range(20):
            # pylint: disable=protected-access
            await queuer._auto_queue_genre(self.mpd)
            self.assertIn(self.mpd.mpd_queue[i], ["J1", "J2", "J3"])

    @patch.object(AutoQueuer, '_requires_new_file', return_value=True)
    async def test_auto_queue_from_genre_with_one_file(self, _: None) -> None:
        """Auto-queue if only 1 file from genre: Always play the same file"""
        self.mpd.mpd_files.append({"file": "J1", "genre": "Jazz"})
        self.mpd.mpd_files.append({"file": "J2", "genre": "Jazz"})
        self.mpd.mpd_files.append({"file": "J3", "genre": "Jazz"})
        self.mpd.mpd_files.append({"file": "J4", "genre": "Blues"})

        self.assertEqual(self.mpd.mpd_queue, [])

        queuer = AutoQueuer(self.mpd, 5, genre='Blues')
        await queuer.auto_queue()
        await queuer.auto_queue()
        await queuer.auto_queue()

        self.assertEqual(self.mpd.mpd_queue, ['J4', 'J4', 'J4'])

    @patch.object(AutoQueuer, '_requires_new_file', return_value=True)
    async def test_auto_queue_from_genre_with_no_files(self, _: None) -> None:
        """Auto-queue if there are no files in genre: Quietly do nothing"""
        self.mpd.mpd_files.append({"file": "J1", "genre": "Jazz"})
        self.mpd.mpd_files.append({"file": "J2", "genre": "Jazz"})
        self.mpd.mpd_files.append({"file": "J3", "genre": "Jazz"})
        self.mpd.mpd_files.append({"file": "J4", "genre": "Blues"})

        self.assertEqual(self.mpd.mpd_queue, [])
        queuer = AutoQueuer(self.mpd, 5, genre='Electro')

        await queuer.auto_queue()
        self.assertEqual(self.mpd.mpd_queue, [])

        await queuer.auto_queue()
        self.assertEqual(self.mpd.mpd_queue, [])


class TestAutoQueueAny(IsolatedAsyncioTestCase):
    """
    Test the generic auto-queue functionality.

    If no genre or playlist have been specified, auto-queue should pick any
    random song from mpd and start playing it.
    """
    def setUp(self) -> None:
        self.mpd = MockMPD()
        self.queuer = AutoQueuer(self.mpd, 5)

    @patch.object(AutoQueuer, '_requires_new_file', return_value=True)
    async def test_auto_queue_any_issues_play_command(self, _: None) -> None:
        """Auto-queue should issue a 'play' command"""
        self.assertEqual(self.mpd.commands, [])

        await self.queuer.auto_queue()
        self.assertEqual(self.mpd.commands, ['play'])

    @patch.object(AutoQueuer, '_requires_new_file', return_value=True)
    async def test_auto_queue_queues_any_by_default(self, _: None) -> None:
        """By default, auto-queue should pick any random song from mpd"""
        # pylint: disable=protected-access
        self.queuer._auto_queue_any = AsyncMock()   # type: ignore

        await self.queuer.auto_queue()
        self.assertEqual(self.queuer._auto_queue_any.call_count, 1)

        await self.queuer.auto_queue()
        self.assertEqual(self.queuer._auto_queue_any.call_count, 2)

    @patch.object(AutoQueuer, '_requires_new_file', return_value=True)
    async def test_auto_queue_does_not_use_any_if_genre(self, _: None) -> None:
        """
        If a genre has been configured, auto-queue should only play songs from
        that genre.
        """
        # pylint: disable=protected-access
        queuer = AutoQueuer(self.mpd, 5, genre='Electro')
        queuer._auto_queue_any = AsyncMock()    # type: ignore
        await queuer.auto_queue()
        queuer._auto_queue_any.assert_not_called()

        queuer = AutoQueuer(self.mpd, 5)
        queuer._auto_queue_any = AsyncMock()    # type: ignore
        await queuer.auto_queue()
        queuer._auto_queue_any.assert_called_once()

    @patch.object(AutoQueuer, '_requires_new_file', return_value=True)
    async def test_auto_queue_any(self, _: None) -> None:
        """Auto queue any random file"""
        self.mpd.mpd_files.append({"file": "334"})
        self.mpd.mpd_files.append({"file": "335"})
        self.mpd.mpd_files.append({"file": "336"})

        self.assertEqual(self.mpd.mpd_queue, [])

        await self.queuer.auto_queue()
        self.assertEqual(len(self.mpd.mpd_queue), 1)
        self.assertIn(self.mpd.mpd_queue[0], ['334', '335', '336'])

        for __ in range(20):
            await self.queuer.auto_queue()

        self.assertEqual(len(self.mpd.mpd_queue), 21)

    @patch.object(AutoQueuer, '_requires_new_file', return_value=True)
    async def test_auto_queue_do_not_play_directory(self, _: None) -> None:
        """Auto queue any random file: Do *not* try to play a directory"""
        self.mpd.mpd_files.append({"directory": "334"})
        self.mpd.mpd_files.append({"directory": "335"})
        self.mpd.mpd_files.append({"directory": "336"})

        self.assertEqual(self.mpd.mpd_queue, [])

        await self.queuer.auto_queue()
        self.assertEqual(self.mpd.mpd_queue, [])

    @patch.object(AutoQueuer, '_requires_new_file', return_value=True)
    async def test_auto_queue_any_does_not_repeat(self, _: None) -> None:
        """Auto-queue should not ever play the same file twice in a row"""
        files = [{'file': str(i)} for i in range(15)]
        self.mpd.mpd_files = files

        for i in range(200):
            await self.queuer.auto_queue()

        for i in range(199):
            self.assertNotEqual(self.mpd.mpd_queue[i], self.mpd.mpd_queue[i+1])

    @patch.object(AutoQueuer, '_requires_new_file', return_value=True)
    async def test_auto_queue_any_single_song(self, _: None) -> None:
        """Auto-queue if only 1 file available: Always play the same file"""
        self.mpd.mpd_files.append({'file': '354'})

        self.assertEqual(self.mpd.mpd_queue, [])

        await self.queuer.auto_queue()
        self.assertEqual(self.mpd.mpd_queue, ['354'])

        await self.queuer.auto_queue()
        self.assertEqual(self.mpd.mpd_queue, ['354', '354'])

        await self.queuer.auto_queue()
        self.assertEqual(self.mpd.mpd_queue, ['354', '354', '354'])

    @patch.object(AutoQueuer, '_requires_new_file', return_value=True)
    async def test_auto_queue_any_no_songs(self, _: None) -> None:
        """Auto-queue if there are no files available: Quietly do nothing"""
        self.mpd.mpd_files = []

        self.assertEqual(self.mpd.mpd_queue, [])

        await self.queuer.auto_queue()
        self.assertEqual(self.mpd.mpd_queue, [])

        await self.queuer.auto_queue()
        self.assertEqual(self.mpd.mpd_queue, [])
