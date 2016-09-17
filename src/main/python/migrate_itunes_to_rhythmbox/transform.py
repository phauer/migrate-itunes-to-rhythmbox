import urllib.parse

# \/:*?"<>| are invalid characters for file names under windows. So we don't have to worry about them.


# old implementation. property location_unescaped was not yet available. took some reverse engineering.
def transform_to_rhythmbox_path_old(location: str, target_library_root: str, source_library_root: str) -> str:
    """ replaces the library root and escapes characters, but not all. prefix with 'file://'"""
    replaced_location = location.replace(source_library_root, target_library_root)
    escaped = urllib.parse.quote(replaced_location, safe="/()!'*:&$=~+,")
    # reverse engineering showed that Rhyhtmbox doesn't escape these safe characters. if escaped they wouldn't be found by rhythmbox.
    # preserve & here because it will later be escaped during xml serialization
    prefixed = "file://{}".format(escaped)
    return prefixed


# using the new location_unescaped property we rely on the path from iTunes, which fits nicely to Rhythmbox' format.
def transform_to_rhythmbox_path(location_unescaped: str, target_library_root: str, source_library_root: str) -> str:
    replaced_location = location_unescaped\
        .replace(source_library_root, target_library_root)\
        .replace("localhost/", "")
    return replaced_location
