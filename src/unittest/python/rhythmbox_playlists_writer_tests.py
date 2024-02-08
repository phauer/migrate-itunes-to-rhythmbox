import unittest

from pathlib import Path

from migrate_itunes_to_rhythmbox import itunes_library_reader, rhythmbox_playlists_writer, settings


class PlaylistTest(unittest.TestCase):
    def setUp(self):
        self.target_folder = Path(settings.TESTOUTPUT_FOLDER).joinpath("PlaylistTest")
        if not self.target_folder.exists():
            self.target_folder.makedirs()

    def write_playlist_and_compare(self, itunes_library_input: Path, expected_playlist_xml: Path):
        target_path = self.target_folder.joinpath(expected_playlist_xml.name)
        itunes_library_path = str(itunes_library_input)
        playlists = itunes_library_reader.read_playlists(itunes_library_path)
        rhythmbox_playlists_writer.write(playlists=playlists,
                                         target_path=target_path,
                                         source_library_root="D:/Music/",
                                         target_library_root="/home/pha/Music/")
        with target_path.open(mode="r", encoding="UTF-8") as target_path_opened, \
                expected_playlist_xml.open("r") as expected_playlist_xml_opened:
            actual_playlist_xml = target_path_opened.read()
            expected_playlist_xml = expected_playlist_xml_opened.read()
        self.assertEqual(actual_playlist_xml, expected_playlist_xml, "{} and {} are different!".format(target_path_opened, expected_playlist_xml))

    def test_happy_path(self):
        self.write_playlist_and_compare(
            itunes_library_input=settings.TEST_RESOURCES_FOLDER.joinpath("input", "playlist", "itunes-library.xml"),
            expected_playlist_xml=settings.TEST_RESOURCES_FOLDER.joinpath("expected_output", "rhythmbox-playlists-modified.xml")
        )

    def test_itunes_library_without_file_locations(self):
        # assert no exception. just skip the songs.
        self.write_playlist_and_compare(
            itunes_library_input=settings.TEST_RESOURCES_FOLDER.joinpath("input", "bug", "itunes-library-without-file-location.xml"),
            expected_playlist_xml=settings.TEST_RESOURCES_FOLDER.joinpath("expected_output", "rhythmbox-playlists-without-file-location.xml")
        )

    def test_exclude_playlist_folders(self):
        target_path = self.target_folder.joinpath("rhythmbox-playlists-with-folders.xml")
        itunes_library_path = str(settings.TEST_RESOURCES_FOLDER.joinpath("input", "playlist", "itunes-library-with-playlist-folders.xml"))
        playlists = itunes_library_reader.read_playlists(itunes_library_path)
        rhythmbox_playlists_writer.write(playlists=playlists,
                                         target_path=target_path,
                                         source_library_root="D:/Music/",
                                         target_library_root="/home/pha/Music/",
                                         exclude_playlist_folders=True)
        with target_path.open(mode="r", encoding="UTF-8") as target_path:
            actual_playlist_xml = target_path.read()

        self.assertTrue("name=\"PlaylistFolder\"" not in actual_playlist_xml, "Playlist folder should be excluded!")
        self.assertTrue("name=\"PlaylistFolder-PlaylistInFolder\"" in actual_playlist_xml, "Playlist of folder should be prefixed with folder name!")
        self.assertTrue("name=\"PlaylistFolder-PlaylistInFolder2\"" in actual_playlist_xml, "Playlist of folder should be prefixed with folder name!")

if __name__ == '__main__':
    unittest.main()

