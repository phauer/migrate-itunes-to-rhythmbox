import unittest
from lxml import etree
from path import Path
from migrate_itunes_to_rhythmbox import itunes_library_reader, rhythmbox_count_rating_integrator, settings
from migrate_itunes_to_rhythmbox.rhythmbox_count_rating_integrator import SongStatistic, IntegrationLog


def sort_and_clean(actual_playlist_xml):
    sorted_string = ''.join(sorted(actual_playlist_xml))
    return sorted_string.replace("\n", "").replace(" ", "")


class CounterIntegrationTest(unittest.TestCase):
    maxDiff = None

    def setUp(self):
        self.target_folder = Path(settings.TESTOUTPUT_FOLDER).joinpath("CounterIntegrationTest")
        if not self.target_folder.exists():
            self.target_folder.makedirs()

    def test_happy_path(self):
        self.set_values_and_compare(rhythmdb_without_cout_rating=settings.TEST_RESOURCES_FOLDER.joinpath("input", "count_rating", "rhythmdb-without-count-ratings-one-track-missing.xml"),
                                    itunes_library_path=settings.TEST_RESOURCES_FOLDER.joinpath("input", "count_rating", "itunes-library-with-count-rating.xml"),
                                    expected_rhythmboxdb=settings.TEST_RESOURCES_FOLDER.joinpath("expected_output", "rhythmdb-count-ratings-one-track-missing.xml"),
                                    output_file_name="happy_path.xml",
                                    assert_something_was_changed=True)

    def test_itunes_track_missing_in_rhythmdb(self):
        self.set_values_and_compare(rhythmdb_without_cout_rating=settings.TEST_RESOURCES_FOLDER.joinpath("input", "count_rating", "rhythmdb-without-count-ratings.xml"),
                                    itunes_library_path=settings.TEST_RESOURCES_FOLDER.joinpath("input", "count_rating", "itunes-library-with-count-rating.xml"),
                                    expected_rhythmboxdb=settings.TEST_RESOURCES_FOLDER.joinpath("expected_output", "rhythmdb-count-ratings.xml"),
                                    output_file_name="itunes_track_missing_in_rhythmdb.xml",
                                    assert_something_was_changed=True)

    def test_itunes_tracks_without_file_location(self):
        # no exception and nothing should be changed
        arbitary_rhythmdb = settings.TEST_RESOURCES_FOLDER.joinpath("input", "count_rating", "rhythmdb-without-count-ratings.xml")
        self.set_values_and_compare(
                                    rhythmdb_without_cout_rating=arbitary_rhythmdb,
                                    itunes_library_path=settings.TEST_RESOURCES_FOLDER.joinpath("input", "bug", "itunes-library-without-file-location.xml"),
                                    expected_rhythmboxdb=arbitary_rhythmdb,
                                    output_file_name="itunes_tracks_without_file_location.xml",
                                    assert_something_was_changed=False)

    # on a mac, the song path in the itunes.xml is different. they don't contain the "localhost" at the start.
    def test_different_path_on_mac(self):
        self.set_values_and_compare(rhythmdb_without_cout_rating=settings.TEST_RESOURCES_FOLDER.joinpath("input", "mac", "rhythmdb-without-count-ratings.xml"),
                                    itunes_library_path=settings.TEST_RESOURCES_FOLDER.joinpath("input", "mac", "itunes-library-with-count-rating.xml"),
                                    expected_rhythmboxdb=settings.TEST_RESOURCES_FOLDER.joinpath("expected_output", "rhythmdb-count-ratings-mac.xml"),
                                    output_file_name="different_path_on_mac.xml",
                                    assert_something_was_changed=True,
                                    itunes_library_root="/Users/Username/Music/iTunes/iTunes%20Music/",
                                    rhythmbox_library_root="/home/Username/Music/iTunes/iTunes%20Music/")

    def set_values_and_compare(self, rhythmdb_without_cout_rating: Path,
                               itunes_library_path: Path,
                               expected_rhythmboxdb:Path,
                               output_file_name: str,
                               assert_something_was_changed: bool,
                               itunes_library_root: str="D:/Music/",
                               rhythmbox_library_root: str="/home/pha/Music/") -> IntegrationLog:
        target_rhythmdb = self.target_folder.joinpath(output_file_name)
        rhythmdb_without_cout_rating.copy(target_rhythmdb)
        itunes_library = str(itunes_library_path)
        songs = itunes_library_reader.read_songs(itunes_library)
        log = rhythmbox_count_rating_integrator.set_values(itunes_songs=songs,
                                                         target_rhythmdb=target_rhythmdb,
                                                         itunes_library_root=itunes_library_root,
                                                         rhythmbox_library_root=rhythmbox_library_root)
        print("Expect something has changed: {}".format(assert_something_was_changed))
        if assert_something_was_changed:
            self.assertTrue(log.something_was_changed(), "No song entries was changed! But they should be!")
        else:
            self.assertFalse(log.something_was_changed(), "A song entries was changed! But they shouldn't be!")

        print("Compare content of {} (actual) with {} (expected)".format(target_rhythmdb, expected_rhythmboxdb))
        with expected_rhythmboxdb.open(mode="r", encoding="UTF-8") as expected_rhythmboxdb_opened, target_rhythmdb.open(
                "r") as target_rhythmdb_opened:
            actual_playlist_xml = target_rhythmdb_opened.read()
            expected_playlist_xml = expected_rhythmboxdb_opened.read()
        # comparing xml is a pain. simple string comparision doesn't work due to different tag order and formatting (newline after each tag or not).
        # so let's sort each character in both xml strings. this leads to rubbish. but if the sorted rubbish is equal, the origin is xml is very likely to be equal.
        actual_playlist_xml_normalized = sort_and_clean(actual_playlist_xml)
        expected_playlist_xml_normalized = sort_and_clean(expected_playlist_xml)
        self.assertEqual(actual_playlist_xml_normalized, expected_playlist_xml_normalized,
                         "Normalized content of {} and {} are different!".format(expected_rhythmboxdb, target_rhythmdb))
        return log


class CounterUnitTest(unittest.TestCase):
    def test_integrate_statistics_into_entry_empty(self):
        song_entry = etree.fromstring('<entry type="song"></entry>')
        itunes_statistic = SongStatistic(play_count=5, rating=3, last_played_timestamp="1474707231")

        rhythmbox_count_rating_integrator.integrate_statistics_into_entry(itunes_statistic, song_entry)
        actual_song_entry = etree.tostring(song_entry).decode('UTF-8')
        expected_song_entry = '<entry type="song"><play-count>5</play-count><rating>3</rating><last-played>1474707231</last-played></entry>'

        self.assertEqual(expected_song_entry, actual_song_entry)

    def test_integrate_statistics_overwrite_if_existing(self):
        song_entry = etree.fromstring('<entry type="song"><play-count>5</play-count><rating>0</rating><last-played>9994707231</last-played></entry>')
        itunes_statistic = SongStatistic(play_count=99, rating=5, last_played_timestamp="1474707231")

        rhythmbox_count_rating_integrator.integrate_statistics_into_entry(itunes_statistic, song_entry)
        actual_song_entry = etree.tostring(song_entry).decode('UTF-8')
        expected_song_entry = '<entry type="song"><play-count>99</play-count><rating>5</rating><last-played>1474707231</last-played></entry>'

        self.assertEqual(expected_song_entry, actual_song_entry)

    def test_integrate_statistics_remove_node_if_not_existing(self):
        song_entry = etree.fromstring('<entry type="song"><play-count>5</play-count><rating>2</rating><last-played>9994707231</last-played></entry>')
        itunes_statistic = SongStatistic(play_count=None, rating=None, last_played_timestamp=None)

        rhythmbox_count_rating_integrator.integrate_statistics_into_entry(itunes_statistic, song_entry)
        actual_song_entry = etree.tostring(song_entry).decode('UTF-8')
        expected_song_entry = '<entry type="song"/>'

        self.assertEqual(expected_song_entry, actual_song_entry)


    def test_create_canonical_location(self):
        # on windows, there is a "localhost" in the itunes path
        self.assert_canonical_locations_are_equal(itunes_path="file://localhost/D:/Music/O.A.R/Live%20On%20Red%20Rocks%20(CD1)/1-03%20Shattered%20(Turn%20The%20Car%20Around).mp3",
                                                  itunes_library_root="D:/Music/",
                                                  rhythmbox_path="file:///home/pha/Music/O.A.R/Live%20On%20Red%20Rocks%20(CD1)/1-03%20Shattered%20(Turn%20The%20Car%20Around).mp3",
                                                  rhythmbox_library_root="/home/pha/Music/")
        # on mac, there is no "localhost" in the itunes path
        self.assert_canonical_locations_are_equal(itunes_path="file:///Users/Username/Music/iTunes/iTunes%20Music/Aerosmith/O,%20Yeah!%20Ultimate%20Aerosmith%20Hits%20(Disc%201)/01%20Mama%20Kin.mp3",
                                                  itunes_library_root="/Users/Username/Music/iTunes/iTunes%20Music/",
                                                  rhythmbox_path="file:///home/Username/Music/iTunes/iTunes%20Music/Aerosmith/O,%20Yeah!%20Ultimate%20Aerosmith%20Hits%20(Disc%201)/01%20Mama%20Kin.mp3",
                                                  rhythmbox_library_root="/home/Username/Music/iTunes/iTunes%20Music/")

    def assert_canonical_locations_are_equal(self, itunes_path: str,
                                             itunes_library_root: str,
                                             rhythmbox_path: str,
                                             rhythmbox_library_root: str):
        location1 = rhythmbox_count_rating_integrator.create_canonical_location_for_itunes_location(itunes_location=itunes_path, itunes_library_root=itunes_library_root)
        location2 = rhythmbox_count_rating_integrator.create_canonical_location_for_rhythmbox(rhythmbox_location=rhythmbox_path, rhythmbox_library_root=rhythmbox_library_root)
        self.assertEqual(location1, location2)

if __name__ == '__main__':
    unittest.main()

