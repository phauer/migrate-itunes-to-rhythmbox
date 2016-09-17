from lxml import etree
from pyItunes import Library, Playlist, Song
from typing import List
from path import Path
from migrate_itunes_to_rhythmbox.transform import transform


def write(playlists: List[Playlist], target_path: Path, target_library_root: str, source_library_root: str) -> None:
    root = etree.Element("rhythmdb-playlists")
    for playlist in playlists:
        attributes = {'name': playlist.name, 'show-browser': 'true', 'browser-position': "231", 'search-type': "search-match", 'type': "static"}
        playlist_element = etree.SubElement(root, "playlist", attributes)
        for song in playlist.tracks:
            transformed_location = transform(song.location, target_library_root, source_library_root)
            location_element = etree.SubElement(playlist_element, "location")
            location_element.text = transformed_location
    write_to_file(root, target_path)


def write_to_file(root, target_path: Path):
    xml_string = etree.tostring(root, pretty_print=True, xml_declaration=True, encoding='UTF-8')
    final_string = xml_string.decode('UTF-8')
    with target_path.open("w") as output_file:
        print(final_string, file=output_file)
