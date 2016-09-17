import unittest
from migrate_itunes_to_rhythmbox import itunes_library_reader, rhythmbox_playlists_writer
from path import Path


class IntegrationTest(unittest.TestCase):
    def setUp(self):
        self.target_folder = Path("../../../target/testoutput/")
        if not self.target_folder.exists():
            self.target_folder.makedirs()

    def test_happy_path(self):
        target_path = self.target_folder.joinpath("rhythmbox-playlists.xml")
        playlists = itunes_library_reader.read_playlists("../resources/input/itunes-library.xml")
        rhythmbox_playlists_writer.write(playlists=playlists,
                                         target_path=target_path,
                                         source_library_root="D:/Music/",
                                         target_library_root="/home/pha/Music/")

        actual_playlist_xml = target_path.open("r").read()
        expected_playlist_xml = Path("../resources/expected_output/rhythmbox-playlists-modified.xml").open("r").read()
        self.assertEqual(actual_playlist_xml, expected_playlist_xml)

    def test_exclude_playlist_folders(self):
        target_path = self.target_folder.joinpath("rhythmbox-playlists-with-folders.xml")
        playlists = itunes_library_reader.read_playlists("../resources/input/itunes-library-with-playlist-folders.xml")
        rhythmbox_playlists_writer.write(playlists=playlists,
                                         target_path=target_path,
                                         source_library_root="D:/Music/",
                                         target_library_root="/home/pha/Music/",
                                         exclude_playlist_folders=True)
        actual_playlist_xml = target_path.open("r").read()
        self.assertTrue("PlaylistFolder" not in actual_playlist_xml, "Playlist folder should be excluded!")

if __name__ == '__main__':
    unittest.main()

