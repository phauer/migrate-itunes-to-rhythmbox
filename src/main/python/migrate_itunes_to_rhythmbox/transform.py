import urllib

# \/:*?"<>| are invalid characters for file names under windows. So we don't have to worry about them.


def transform(location: str, target_library_root: str, source_library_root: str) -> str:
    """ replaces the library root and escapes characters, but not all. prefix with 'file://'"""
    replaced_location = location.replace(source_library_root, target_library_root)
    escaped = urllib.parse.quote(replaced_location, safe="/()!'*:&$=~+")
    # reverse engineering showed that rhyhtmbox doesn't escape these safe characters. if escaped they wouldn't be found by rhythmbox.
    # preserve & here because it will later be escaped during xml serialization
    prefixed = "file://{}".format(escaped)
    return prefixed
