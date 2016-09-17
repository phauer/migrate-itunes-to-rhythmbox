- folder-related
    - prefix playlist name with folder!
    - don't copy folders.
    - therefore:
    - fork pyitunes: add properties to Playlist:
        <key>Folder</key><true/>
        <key>Playlist Persistent ID</key><string>2FF04777ECDBAB71</string>
        <key>Parent Persistent ID</key><string>B01923CD687E0E29</string>
        moreover: location_unescaped (itunes escapes like rhythmbox, except for &. so it would have been helpful)
- README "install and usage" via pip install <path to uploaded tar.gz on github>
- migrate count and ratings