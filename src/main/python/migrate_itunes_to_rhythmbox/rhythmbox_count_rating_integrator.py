from libpytunes import Song
from typing import List, Dict
from pathlib import Path
import lxml.etree
from migrate_itunes_to_rhythmbox import common
from time import struct_time
import calendar

# different rating scales. itunes: 0 (no star) - 100 (5 stars). rhythmbox: 0-5.
ITUNES_TO_RHYTHMBOX_RATINGS_MAP = {0: 0, 20: 1, 40: 2, 60: 3, 80: 4, 100: 5, None: None}


class SongStatistic:
    def __init__(self, play_count: int, rating: int, last_played_timestamp: str, date_added_timestamp: str):
        self.play_count = play_count
        self.rating = rating
        self.last_played_timestamp = last_played_timestamp
        self.date_added_timestamp = date_added_timestamp


class IntegrationLog:
    def __init__(self):
        self.rhythmbox_song_entries_changed = 0

    def increment_changed_song_counter(self):
        self.rhythmbox_song_entries_changed += 1

    def something_was_changed(self) -> bool:
        return self.rhythmbox_song_entries_changed != 0


def set_values(itunes_songs: Dict[int, Song], target_rhythmdb: Path, itunes_library_root: str, rhythmbox_library_root: str) -> IntegrationLog:
    itunes_statistics_dict = create_itunes_statistic_dict(itunes_songs, itunes_library_root)

    rhythmdb = lxml.etree.parse(target_rhythmdb)
    root = rhythmdb.getroot()
    log = integrate_statistics_into_rhythmdb(root, itunes_statistics_dict, rhythmbox_library_root)

    if log.something_was_changed():
        common.write_to_file(root, target_rhythmdb, add_standalone_to_xml_declaration=True)
    return log


def integrate_statistics_into_rhythmdb(root, itunes_statistics_dict: Dict[str, SongStatistic], rhythmbox_library_root: str) -> IntegrationLog:
    log = IntegrationLog()
    rhythmdb_song_entries = root.getchildren()
    for rhythmdb_song_entry in rhythmdb_song_entries:
        location = rhythmdb_song_entry.find("location").text
        canonical_location = create_canonical_location_for_rhythmbox(location, rhythmbox_library_root)
        if canonical_location in itunes_statistics_dict:
            itunes_statistics = itunes_statistics_dict[canonical_location]
            integrate_statistics_into_entry(itunes_statistics, rhythmdb_song_entry)
            log.increment_changed_song_counter()
    return log


def integrate_statistics_into_entry(itunes_statistics, rhythmdb_song_entry):
    integrate_value_to_rhythmdb_song_entry(rhythmdb_song_entry, "play-count", itunes_statistics.play_count)
    integrate_value_to_rhythmdb_song_entry(rhythmdb_song_entry, "rating", itunes_statistics.rating)
    integrate_value_to_rhythmdb_song_entry(rhythmdb_song_entry, "last-played", itunes_statistics.last_played_timestamp)
    integrate_value_to_rhythmdb_song_entry(rhythmdb_song_entry, "first-seen", itunes_statistics.date_added_timestamp)


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
        if itunes_song.location_escaped is not None:
            count = itunes_song.play_count
            last_played = itunes_song.lastplayed
            last_played_timestamp = calendar.timegm(last_played) if last_played is not None else None
            date_added = itunes_song.date_added
            date_modified = itunes_song.date_modified
            if date_modified < date_added:
                date_added = date_modified #somehow I messed up the timestamps on my library back in 2011
            date_added_timestamp = calendar.timegm(date_added) if date_added is not None else None
            itunes_rating = itunes_song.rating
            mapped_rating = ITUNES_TO_RHYTHMBOX_RATINGS_MAP[itunes_rating]
            location = itunes_song.location_escaped
            canonical_location = create_canonical_location_for_itunes_location(location, itunes_library_root)
            dict[canonical_location] = SongStatistic(count, mapped_rating, last_played_timestamp, date_added_timestamp)
        else:
            print("   Can't assign the track [{} - {}] because there is no file location defined. It's probably a remote file."
                  .format(itunes_song.artist, itunes_song.name))
    return dict

PREFIX_ITUNES_ON_WINDOWS = "file://localhost/"
PREFIX_ITUNES_ON_MAC = "file://"
PREFIX_RHYTHMBOX = "file://"


def create_canonical_location_for_itunes_location(itunes_location: str, itunes_library_root: str):
    # don't mix up order
    if itunes_location.startswith(PREFIX_ITUNES_ON_WINDOWS):
        return itunes_location.replace(PREFIX_ITUNES_ON_WINDOWS + itunes_library_root, "")
    if itunes_location.startswith(PREFIX_ITUNES_ON_MAC):
        return itunes_location.replace(PREFIX_ITUNES_ON_MAC + itunes_library_root, "")
    print("""   The itunes location {} doesn't start with a known prefix.
    It's likely that we can't match it later to a rhythmbox path.""".format(itunes_location))
    return itunes_location


def create_canonical_location_for_rhythmbox(rhythmbox_location: str, rhythmbox_library_root: str):
    if rhythmbox_location.startswith(PREFIX_RHYTHMBOX):
        return rhythmbox_location.replace(PREFIX_RHYTHMBOX + rhythmbox_library_root, "")
    print("""   The rhythmbox location {} doesn't start with a known prefix.
    It's likely that we can't match it later to a itunes path.""".format(rhythmbox_location))
    return rhythmbox_location