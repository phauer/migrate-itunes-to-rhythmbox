from libpytunes import Library, Playlist, Song
from typing import List, Dict

english_german_ignore_list = ("Library", "Music", "Movies", "TV Shows", "Purchased", "iTunes DJ", "Podcasts",
                            "Mediathek", "Musik", "Filme", "TV-Sendungen", "iTunes U", "Bücher", "Töne", "Genius")


def read_playlists(library_file: str) -> List[Playlist]:
    library = Library(library_file)
    playlist_names = library.getPlaylistNames(ignoreList=english_german_ignore_list)
    return [library.getPlaylist(playlist_name) for playlist_name in playlist_names]


def read_songs(library_file: str) -> Dict[int, Song]:
    library = Library(library_file)
    return library.songs
