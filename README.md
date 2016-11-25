# Migrate iTunes to Rhythmbox

Script to migrate iTunes **playlists, play counts, ratings and last played date** to Rhythmbox.

![Convert iTunes playlists, play counts and ratings to Rhyhtmbox](featured_image.png)

Tested with:
- iTunes 12.5.1
- Rhythmbox 3.3, 3.4

Does the script work with a newer version of iTunes or Rhythmbox? Please let me know by opening an issue. 

## Installation
You need at least Python 3.5! Check it via `$ python3 --version`

Install pip if you haven't already.
```
sudo apt install python3-pip 
```
Install _migrate-itunes-to-rhythmbox_
```
$ pip3 install https://github.com/phauer/migrate-itunes-to-rhythmbox/releases/download/1.0.3/migrate-itunes-to-rhythmbox-1.0.3.tar.gz --process-dependency-links --user
```
The script is now installed to `.local/bin/migrate-itunes-to-rhythmbox`. You may want to add `~/.local/bin` to your $PATH:
```
echo 'export PATH=~/.local/bin:$PATH' >> ~/.profile 
```
Log out and in again. Afterwards, you can call the script via:
```
$ migrate-itunes-to-rhythmbox --help
```
## Usage

### Preparation
You have to install Rhythmbox and import your Music folder **before** you use _migrate-itunes-to-rhythmbox_. 
Just place your music under `~/Music` and Rhythmbox will automatically add your music files on start up.

You also need your iTunes Library in the XML format. You can export the file in iTunes with `File > Library > Export Library...`.
You may also find the XML file under `<Music Folder>/iTunes/iTunes Music Library.xml`. 

### Migrate Playlists
```
Usage: migrate-itunes-to-rhythmbox playlists [OPTIONS]

  Reads the playlists from iTunes and converts them to Rhythmbox' format.
  Moreover, it replaces the root path of your library.

Options:
  --itunes_library_xml TEXT       Path to the source iTunes library xml
                                  (iTunes Library.xml or iTunes Music
                                  Library.xml). Can be exported in iTunes with
                                  'File > Library > Export Library...'
  --rhythmbox_playlists_xml TEXT  Target Path for the created Rhythmbox
                                  playlist.xml'
  --source_library_root TEXT      Root path path of the iTunes-based library.
                                  Will be replaced with <target_library_root>
  --target_library_root TEXT      Root path path of the Rhythmbox-based
                                  library. Replaces the value of
                                  <source_library_root>
  --exclude_playlist_folders BOOLEAN
                                  Exclude playlist folders. Otherwise you will
                                  have the sub playlists AND a playlist for
                                  the folder containing also all tracks from
                                  the sub playlists. Defaults to true.
  --help                          Show this message and exit.
```

#### Examples

```
$ migrate-itunes-to-rhythmbox playlists --help

# example:
$ migrate-itunes-to-rhythmbox playlists \
    --itunes_library_xml="~/Music/iTunes/iTunes Music Library.xml" \
    --rhythmbox_playlists_xml="~/.local/share/rhythmbox/playlists.xml" \
    --source_library_root="D:/Music/" \
    --target_library_root="/home/pha/Music/"

# example, where iTunes library lies under "C:/Users/(username)/Music/iTunes/iTunes%20Media/Music/" which is quite common
migrate-itunes-to-rhythmbox playlists \
    --itunes_library_xml="~/iTunes/iTunes Music Library.xml" \
    --rhythmbox_playlists_xml="~/.local/share/rhythmbox/playlists.xml" \
    --source_library_root="C:/Users/(username)/Music/iTunes/iTunes%20Media/Music/" \
    --target_library_root="/home/(username)/Music/"

# Use relative paths. Assumes that the "iTunes Library.xml" is in current directory and "rhythmbox-playlists.xml" will also placed there.
$ migrate-itunes-to-rhythmbox playlists \
    --itunes_library_xml="iTunes Library.xml" \
    --rhythmbox_playlists_xml="rhythmbox-playlists.xml" \
    --source_library_root="D:/Music/" \
    --target_library_root="/home/pha/Music/"
```

#### Troubleshooting

##### The created playlists are empty in Rhythmbox
Please check your xxxx_library_root parameters! Let's assume the following parameters:

- `--itunes_library_xml="~/iTunes/iTunes Music Library.xml"`
- **`--source_library_root="C:/Users/(username)/Music/iTunes/iTunes%20Media/Music/"`**
- **`--target_library_root="/home/(username)/Music/"`**
- `--rhythmbox_playlists_xml="~/.local/share/rhythmbox/playlists.xml"`

Basically, the script will take the song paths in your `~/iTunes/iTunes Music Library.xml` and replaces the `source_library_root` part with the value of `target_library_root`. The created path is written to the `~/.local/share/rhythmbox/playlists.xml`.
However, the created paths should be the same as in your `~/.local/share/rhythmbox/rhythmdb.xml`. If there is a song path in a playlist but this path can't be found in the `rhythmdb.xml`, Rhythmbox won't show the song in the playlist.

Bottom line: 
- Compare the paths in the created `playlists.xml` with the ones in `~/.local/share/rhythmbox/rhythmdb.xml`. They have to match exactly! 
- Ensure that there really _is_ the `source_library_root` value in the paths in your `--itunes_library_xml`. Given `--source_library_root="C:/Users/(username)/Music/iTunes/iTunes%20Media/Music/"` the paths have to start with `file://localhost/C:/Users/(username)/Music/iTunes/iTunes%20Media/Music/`.
- Ensure that the `target_library_root` value matches to the paths in the `~/.local/share/rhythmbox/rhythmdb.xml`. Given `target_library_root=/home/(username)/Music/` the paths have to start with `file:///home/(username)/Music/`.

### Migrate Play Counts, Ratings and Last Played Date
```
Usage: migrate-itunes-to-rhythmbox counts-ratings [OPTIONS]

  Reads the play counts, ratings and played-last-date from iTunes and adds
  them to Rhythmbox' database. Overrides existing values.

Options:
  --itunes_library_xml TEXT   Path to the source iTunes library xml (iTunes
                              Library.xml or iTunes Music Library.xml). Can be
                              exported in iTunes with 'File > Library > Export
                              Library...'
  --rhythmdb TEXT             Rhythmbox' database, where the data will be
                              added. Please mind that this file will be
                              changed. Maybe you should back up it up front.
  --source_library_root TEXT  Root path path of the iTunes-based library.
  --target_library_root TEXT  Root path path of the Rhythmbox-based library.
  --help                      Show this message and exit.
```

Examples:
```
$ migrate-itunes-to-rhythmbox counts-ratings --help

$ migrate-itunes-to-rhythmbox counts-ratings \
    --itunes_library_xml="~/Music/iTunes/iTunes Music Library.xml" \
    --rhythmdb="~/.local/share/rhythmbox/rhythmdb.xml" \
    --source_library_root="D:/Music/" \
    --target_library_root="/home/pha/Music/"
```

## Deinstallation
```
$ pip3 uninstall migrate-itunes-to-rhythmbox
```

# Development

### Getting Started
The script requires Python 3.5.

Install pip and venv if you haven't already.
```
$ sudo apt install python3-pip python3-venv
```

Project Setup:
```
# git clone and move to project directory
$ pyvenv venv
$ source init.sh # inits venv and sets PYTHONPATH
$ pip install pybuilder
$ pyb # install dependencies, runs tests and builds the project
# ...
$ deactivate # deactivates venv
```

Execution: You can either execute via your IDE or via the shell:
```
$ .init.sh # inits venv and sets PYTHONPATH

# CLI 
$ cd src/main/scripts
$ ./migrate-itunes-to-rhythmbox --help

# Tests
$ cd src/unittest/python
$ python3 integraton_tests.py
```

### Setting up IntelliJ IDEA/PyCharm
- Configure the venv:
  - `File > Project Structure > Project > Project SDK > Add Local`
  - Set path to `<path>/<project root>/venv/bin/python3`
- Python Facet
  - `File > Project Structure > Facets`. Add Python Facet and set interpreter of venv
- `Project Structure... > Modules`. Mark `src/main/python` and `src/unittest/python` as source/test folder. Mark `target` as excluded folder. Mark `src/unittest/resources` as test resources. 
- Sometimes IDEA doesn't seem to recompile all Python files. Setting the output path may help. `Project Structure > Modules > Paths > Use module compile output path`.