# Migrate iTunes to Rhythmbox

Script to Migrate iTunes Playlists to Rhythmbox

Tested with:
- iTunes 12.5.1
- Rhythmbox 3.3

## Preparation
You have to install Rhythmbox and import the content of you Music folder in it. Migrate-itunes-to-rhythmbox will import your playlists.

## Installation
Install pip if you haven't already.
```
sudo apt install python-pip 
```
Install migrate-itunes-to-rhythmbox
```
# git clone and cd into dir
$ pyb
$ pip install target/dist/migrate-itunes-to-rhythmbox-1.0.dev0/dist/migrate-itunes-to-rhythmbox-1.0.dev0.tar.gz 
# optionally add "~/.local/bin" to PATH
# test via:
$ migrate-itunes-to-rhythmbox --help
```
## Usage
```
Usage: migrate-itunes-to-rhythmbox [OPTIONS]

  Reads the playlists from iTunes and converts them to Rhythmbox' format.
  Moreover, it replaces the root path of your library.

Options:
  --itunes_library_xml TEXT       Path to the source iTunes library xml
                                  (iTunes Library.xml or iTunes Music
                                  Library.xml). Can be exported in iTunes with
                                  'File > Library > Export Library'
  --rhythmbox_playlists_xml TEXT  Target Path for the created Rhythmbox
                                  playlist.xml'
  --source_library_root TEXT      Root path path of the iTunes-based library.
                                  Will be replaced with <target_library_root>
  --target_library_root TEXT      Root path path of the Rhythmbox-based
                                  library. Replaces the value of
                                  <source_library_root>
  --help                          Show this message and exit.
```

Examples:

```
# get documentation about the parameter
$ migrate-itunes-to-rhythmbox --help

# places the created rhythmbox to "~/.local/share/rhythmbox/playlists.xml"
$ migrate-itunes-to-rhythmbox --itunes_library_xml="~/Music/iTunes/iTunes Music Library.xml" --source_library_root="D:/Music/" --target_library_root="/home/pha/Music/"

# define rhythmbox_playlists_xml explicitly
$ migrate-itunes-to-rhythmbox --itunes_library_xml="~/Music/iTunes/iTunes Music Library.xml" --rhythmbox_playlists_xml="~/.local/share/rhythmbox/playlists.xml" --source_library_root="D:/Music/" --target_library_root="/home/pha/Music/"

# relative paths. "iTunes Library.xml" is in current directory and "rhythmbox-playlists.xml" will also placed there.
$ migrate-itunes-to-rhythmbox --itunes_library_xml="iTunes Library.xml" --rhythmbox_playlists_xml="rhythmbox-playlists.xml" --source_library_root="D:/Music/" --target_library_root="/home/pha/Music/"
```

## Deinstallation
```
pip uninstall migrate-itunes-to-rhythmbox
```

# Development

### Getting Started
- requires Python 3.5. Test with `python3 --version`.

Install pip and venv if you haven't already.
```
$ sudo apt install python-pip
$ sudo apt install python3-venv 
```

Project:
```
# git clone and move to project directory
$ python3 -m venv venv
$ . init.sh
$ pip install pybuilder
$ pyb install_dependencies
$ pyb # runs tests and builds the project
# ...
$ deactivate # deactivates venv
```

### Setting up IntelliJ IDEA/PyCharm
- Configure the venv:
  - File > Project Structure > Project > Project SDK > Add Local
  - Set path to `<path>/<project root>/venv/bin/python3`
- Python Facet
  - File > Project Structure > Facets. Add Python Facet and set interpreter of venv
- `Project Structure... > Modules`. Mark `src/main/python` and `src/unittest/python` as source folder. Mark `target` as excluded folder.
- Sometimes, IDEA doesn't seem to recompile all Python files. Setting the output path may help. 'Project Structure > Modules > Paths > Use module compile output path'.