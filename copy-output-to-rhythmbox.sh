#!/usr/bin/env bash
rhythmboxDir="~/.local/share/rhythmbox/"
cp "$rhythmboxDir""playlists.xml" "$rhythmboxDir""playlists.xml.bak"
cp target/testoutput/rhythmbox-playlists.xml "$rhythmboxDir""playlists.xml"