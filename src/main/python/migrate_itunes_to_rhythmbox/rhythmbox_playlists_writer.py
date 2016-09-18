from lxml import etree
from pyItunes import Playlist
from typing import List
from path import Path
from migrate_itunes_to_rhythmbox.transform import transform_to_rhythmbox_path


def write(playlists: List[Playlist], target_path: Path, target_library_root: str, source_library_root: str, exclude_playlist_folders: bool = True) -> None:
    root = etree.Element("rhythmdb-playlists")
    filtered_playlist = filter_playlists_if_necessary(playlists, exclude_playlist_folders)
    for playlist in filtered_playlist:
        attributes = {'name': playlist.name, 'show-browser': 'true', 'browser-position': "231",
                      'search-type': "search-match", 'type': "static"}
        playlist_element = etree.SubElement(root, "playlist", attributes)
        for song in playlist.tracks:
            transformed_location = transform_to_rhythmbox_path(song.location_escaped, target_library_root, source_library_root)
            # transformed_location = transform_to_rhythmbox_path(song.location, target_library_root, source_library_root)
            location_element = etree.SubElement(playlist_element, "location")
            location_element.text = transformed_location
    write_to_file(root, target_path)


def filter_playlists_if_necessary(playlists: List[Playlist], exclude_playlist_folders: bool) -> List[Playlist]:
    if exclude_playlist_folders:
        return [playlist for playlist in playlists if not playlist.is_folder]
    return playlists


def write_to_file(root, target_path: Path):
    xml_string = etree.tostring(root, pretty_print=True, xml_declaration=True, encoding='UTF-8')
    final_string = xml_string.decode('UTF-8')
    with target_path.open("w") as output_file:
        print(final_string, file=output_file)
