from lxml import etree
from pyItunes import Playlist
from typing import List, Dict
from path import Path
from migrate_itunes_to_rhythmbox.transform import transform_to_rhythmbox_path


def create_persistent_id_to_playlist_dict(playlists: List[Playlist]) -> Dict[str, Playlist]:
    persistent_id_to_playlist_dict = {}
    for playlist in playlists:
        persistent_id_to_playlist_dict[playlist.playlist_persistent_id] = playlist
    return persistent_id_to_playlist_dict


def create_playlist_name(playlist: Playlist, persistent_id_to_playlist_dict: Dict[str, Playlist]) -> str:
    """prefix with folder name if there is a folder"""
    if playlist.parent_persistent_id is not None:
        parent_playlist = persistent_id_to_playlist_dict[playlist.parent_persistent_id]
        return "{}-{}".format(parent_playlist.name, playlist.name)
    return playlist.name


def write(playlists: List[Playlist], target_path: Path, target_library_root: str, source_library_root: str, exclude_playlist_folders: bool = True) -> None:
    persistent_id_to_playlist_dict = create_persistent_id_to_playlist_dict(playlists)
    filtered_playlist = filter_playlists_if_necessary(playlists, exclude_playlist_folders)
    root = etree.Element("rhythmdb-playlists")
    for playlist in filtered_playlist:
        name = create_playlist_name(playlist, persistent_id_to_playlist_dict)
        attributes = {'name': name, 'show-browser': 'true', 'browser-position': "231",
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
