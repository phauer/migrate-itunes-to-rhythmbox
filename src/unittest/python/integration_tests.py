import unittest
from migrate_itunes_to_rhythmbox import itunes_library_reader, rhythmbox_playlists_writer
from path import Path


class IntegrationTest(unittest.TestCase):
    def test_happy_path(self):
        target_path = Path("../../../target/testoutput/rhythmbox-playlists.xml")
        if not target_path.parent.exists():
            target_path.parent.makedirs()
        playlists = itunes_library_reader.read_playlists("../resources/input/itunes-library.xml")
        rhythmbox_playlists_writer.write(playlists=playlists,
                                         target_path=target_path,
                                         source_library_root="D:/Music/",
                                         target_library_root="/home/pha/Music/")

        actual_playlist_xml = target_path.open("r").read()
        expected_playlist_xml = Path("../resources/expected_output/rhythmbox-playlists-modified.xml").open("r").read()
        self.assertEqual(actual_playlist_xml, expected_playlist_xml)


if __name__ == '__main__':
    unittest.main()

