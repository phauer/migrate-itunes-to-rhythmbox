import unittest

from path import Path

from migrate_itunes_to_rhythmbox import itunes_library_reader, rhythmbox_count_rating_integrator, settings


class CounterTest(unittest.TestCase):
    def setUp(self):
        self.target_folder = Path(settings.TESTOUTPUT_FOLDER)
        if not self.target_folder.exists():
            self.target_folder.makedirs()

    def test_happy_path(self):
        target_rhythmdb = self.target_folder.joinpath("rhythmdb-cout-ratings.xml")
        rhythmdb_without_cout_rating = settings.TEST_RESOURCES_FOLDER.joinpath("input", "count_rating", "rhythmdb-without-count-ratings.xml")
        rhythmdb_without_cout_rating.copy(target_rhythmdb)

        itunes_library = str(settings.TEST_RESOURCES_FOLDER.joinpath("input", "count_rating", "itunes-library-with-count-rating.xml"))
        songs = itunes_library_reader.read_songs(itunes_library)
        rhythmbox_count_rating_integrator.set_values(itunes_songs=songs,
                                                     target_rhythmdb=target_rhythmdb,
                                                     itunes_library_root="D:/Music/",
                                                     rhythmbox_library_root="/home/pha/Music/")

        expected_rhythmboxdb = settings.TEST_RESOURCES_FOLDER.joinpath("expected_output", "rhythmdb-count-ratings.xml")
        with expected_rhythmboxdb.open(mode="r", encoding="UTF-8") as expected_rhythmboxdb, target_rhythmdb.open("r") as target_rhythmdb:
            actual_playlist_xml = target_rhythmdb.read()
            expected_playlist_xml = expected_rhythmboxdb.read()
        self.assertEqual(actual_playlist_xml, expected_playlist_xml)


if __name__ == '__main__':
    unittest.main()

