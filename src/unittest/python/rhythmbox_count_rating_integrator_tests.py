import unittest
from lxml import etree
from path import Path
from migrate_itunes_to_rhythmbox import itunes_library_reader, rhythmbox_count_rating_integrator, settings
from migrate_itunes_to_rhythmbox.rhythmbox_count_rating_integrator import SongStatistic


def sort_and_clean(actual_playlist_xml):
    sorted_string = ''.join(sorted(actual_playlist_xml))
    return sorted_string.replace("\n", "").replace(" ", "")


class CounterIntegrationTest(unittest.TestCase):
    maxDiff = None

    def setUp(self):
        self.target_folder = Path(settings.TESTOUTPUT_FOLDER)
        if not self.target_folder.exists():
            self.target_folder.makedirs()

    def test_happy_path(self):
        self.set_values_and_compare(rhythmdb_without_cout_rating=settings.TEST_RESOURCES_FOLDER.joinpath("input", "count_rating", "rhythmdb-without-count-ratings-one-track-missing.xml"),
                                    itunes_library_path=settings.TEST_RESOURCES_FOLDER.joinpath("input", "count_rating", "itunes-library-with-count-rating.xml"),
                                    expected_rhythmboxdb=settings.TEST_RESOURCES_FOLDER.joinpath("expected_output", "rhythmdb-count-ratings-one-track-missing.xml"))

    def test_itunes_track_missing_in_rhythmdb(self):
        self.set_values_and_compare(rhythmdb_without_cout_rating=settings.TEST_RESOURCES_FOLDER.joinpath("input", "count_rating", "rhythmdb-without-count-ratings.xml"),
                                    itunes_library_path=settings.TEST_RESOURCES_FOLDER.joinpath("input", "count_rating", "itunes-library-with-count-rating.xml"),
                                    expected_rhythmboxdb=settings.TEST_RESOURCES_FOLDER.joinpath("expected_output", "rhythmdb-count-ratings.xml"))

    def set_values_and_compare(self, rhythmdb_without_cout_rating: Path, itunes_library_path: Path, expected_rhythmboxdb:Path):
        target_rhythmdb = self.target_folder.joinpath(str(rhythmdb_without_cout_rating.name))
        rhythmdb_without_cout_rating.copy(target_rhythmdb)
        itunes_library = str(itunes_library_path)
        songs = itunes_library_reader.read_songs(itunes_library)
        rhythmbox_count_rating_integrator.set_values(itunes_songs=songs,
                                                     target_rhythmdb=target_rhythmdb,
                                                     itunes_library_root="D:/Music/",
                                                     rhythmbox_library_root="/home/pha/Music/")
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

if __name__ == '__main__':
    unittest.main()

