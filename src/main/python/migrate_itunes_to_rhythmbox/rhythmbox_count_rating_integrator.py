from pyItunes import Song
from typing import List, Dict
from path import Path
import lxml.etree
from migrate_itunes_to_rhythmbox import common
from time import struct_time
import calendar

# different rating scales. itunes: 0 (no star) - 100 (5 stars). rhythmbox: 0-5.
ITUNES_TO_RHYTHMBOX_RATINGS_MAP = {0: 0, 20: 1, 40: 2, 60: 3, 80: 4, 100: 5, None: None}


class SongStatistic:
    def __init__(self, play_count: int, rating: int, last_played: struct_time):
        self.play_count = play_count
        self.rating = rating
        self.last_played = last_played


def set_count_values(itunes_songs: Dict[int, Song], target_rhythmdb: Path, itunes_library_root: str, rhythmbox_library_root: str) -> None:
    itunes_statistics_dict = create_itunes_statistic_dict(itunes_songs, itunes_library_root)

    rhythmdb = lxml.etree.parse(target_rhythmdb)
    root = rhythmdb.getroot()
    integrate_statistics_into_rhythmdb(root, itunes_statistics_dict, rhythmbox_library_root)

    common.write_to_file(root, target_rhythmdb)


def integrate_statistics_into_rhythmdb(root, itunes_statistics_dict: Dict[str, SongStatistic], rhythmbox_library_root: str):
    rhythmdb_song_entries = root.getchildren()
    for rhythmdb_song_entry in rhythmdb_song_entries:
        location = rhythmdb_song_entry.find("location").text
        canonical_location = location.replace("file://{}".format(rhythmbox_library_root), "")
        if canonical_location in itunes_statistics_dict:
            itunes_statistics = itunes_statistics_dict[canonical_location]
            last_played = calendar.timegm(itunes_statistics.last_played) if itunes_statistics.last_played is not None else None
            integrate_value_to_rhythmdb_song_entry(rhythmdb_song_entry, "play-count", itunes_statistics.play_count)
            integrate_value_to_rhythmdb_song_entry(rhythmdb_song_entry, "rating", itunes_statistics.rating)
            integrate_value_to_rhythmdb_song_entry(rhythmdb_song_entry, "last-played", last_played)


def integrate_value_to_rhythmdb_song_entry(rhythmdb_song_entry, rhythmdb_node_name, itunes_value):
    rhythmdb_value_node = rhythmdb_song_entry.find(rhythmdb_node_name)
    if itunes_value is None and rhythmdb_value_node is not None:
        rhythmdb_song_entry.remove(rhythmdb_value_node)
    elif itunes_value is not None and rhythmdb_value_node is None:
        rhythmdb_value_node = lxml.etree.SubElement(rhythmdb_song_entry, rhythmdb_node_name)
        rhythmdb_value_node.text = str(itunes_value)
    elif itunes_value is not None and rhythmdb_value_node is not None:
        rhythmdb_value_node.text = str(itunes_value)


def create_itunes_statistic_dict(itunes_songs: Dict[int, Song], itunes_library_root: str) -> Dict[str, SongStatistic]:
    """use canonical location as a common identifier. returns dict[canonical_location -> SongStatistic(play_count, rating)]"""
    dict = {}
    for itunes_song in itunes_songs.values():
        count = itunes_song.play_count
        last_played = itunes_song.lastplayed
        itunes_rating = itunes_song.rating
        mapped_rating = ITUNES_TO_RHYTHMBOX_RATINGS_MAP[itunes_rating]
        location = itunes_song.location_escaped
        canonical_location = location.replace("file://localhost/{}".format(itunes_library_root), "")
        dict[canonical_location] = SongStatistic(count, mapped_rating, last_played)
    return dict

