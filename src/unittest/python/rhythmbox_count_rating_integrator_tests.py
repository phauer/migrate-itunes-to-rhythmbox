import unittest

from path import Path

from migrate_itunes_to_rhythmbox import itunes_library_reader, rhythmbox_count_rating_integrator, settings


def sort_and_clean(actual_playlist_xml):
    sorted_string = ''.join(sorted(actual_playlist_xml))
    return sorted_string.replace("\n", "").replace(" ", "")


class CounterTest(unittest.TestCase):
    maxDiff = None
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
        with expected_rhythmboxdb.open(mode="r", encoding="UTF-8") as expected_rhythmboxdb_opened, target_rhythmdb.open("r") as target_rhythmdb_opened:
            actual_playlist_xml = target_rhythmdb_opened.read()
            expected_playlist_xml = expected_rhythmboxdb_opened.read()
        # comparing xml is a pain. simple string comparision doesn't work due to different tag order and formatting (newline after each tag or not).
        # so let's sort each character in both xml strings. this leads to rubbish. but if the sorted rubbish is equal, the origin is xml is very likely to be equal.
        actual_playlist_xml_normalized = sort_and_clean(actual_playlist_xml)
        expected_playlist_xml_normalized = sort_and_clean(expected_playlist_xml)
        self.assertEqual(actual_playlist_xml_normalized, expected_playlist_xml_normalized, "Normalized content of {} and {} are different!".format(expected_rhythmboxdb, target_rhythmdb))

if __name__ == '__main__':
    unittest.main()

