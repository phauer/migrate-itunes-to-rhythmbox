import urllib.parse
import os

# reverse engineering showed that Rhyhtmbox doesn't escape these safe characters. if escaped they wouldn't be found by rhythmbox.
# preserve & here because it will later be escaped during xml serialization
# \/:*?"<>| are invalid characters for file names under windows. So we don't have to worry about them.
SAFE_CHARS = "/()!'*:&$=~+,"

# old implementation. property location_escaped was not yet available. took some reverse engineering.
def transform_to_rhythmbox_path_old(location: str, target_library_root: str, source_library_root: str) -> str:
    """ replaces the library root and escapes characters, but not all. prefix with 'file://'"""
    replaced_location = location.replace(source_library_root, target_library_root)
    escaped = urllib.parse.quote(replaced_location, safe=SAFE_CHARS)
    prefixed = "file://{}".format(escaped)
    return prefixed


# using the new location_escaped property we rely on the already escaped path from iTunes, which fits nicely to Rhythmbox' format.
def transform_to_rhythmbox_path(location_escaped: str, target_library_root: str, source_library_root: str) -> str:
    replaced_location = location_escaped\
        .replace(source_library_root, target_library_root)\
        .replace("localhost/", "")

    # Windows does not care about casing. So shouldn't we
    try:
        fixed_case_location = fix_location_casing(replaced_location)
    except ValueError:
        print(f"  Unable to find a file at path {replaced_location}")
        fixed_case_location = replaced_location

    return fixed_case_location


def fix_location_casing(escaped_path: str):
    unescaped = urllib.parse.unquote(escaped_path).removeprefix("file://")
    correct_path = match_lowercase_path(unescaped.lower())

    if correct_path == unescaped:
        return escaped_path

    else:
        print(f"  Fixed casing for {unescaped} -> {correct_path}")
        quoted = urllib.parse.quote(correct_path, safe=SAFE_CHARS)
        return f"file://{quoted}"


# Taken from https://stackoverflow.com/a/39891399
def match_lowercase_path(path):
    # get absolute path
    path = os.path.abspath(path)

    # try it first
    if os.path.exists(path):
        correct_path = path
    # no luck
    else:
        # works on linux, but there must be a better way
        components = path.split('/')

        # initialise answer
        correct_path = ''

        # step through
        for c in components:
            if os.path.isdir(correct_path + c + '/'):
                correct_path += c +'/'
            elif os.path.isfile(correct_path + c):
                correct_path += c
            else:
                match = find_match(correct_path, c)
                correct_path += match

    return correct_path

# Taken from https://stackoverflow.com/a/39891399
def find_match(path, ext):
    for child in os.listdir(path):
        if child.lower() == ext:
            if os.path.isdir(path + child):
                return child + '/'
            else:
                return child
    else:
        raise ValueError('Could not find a path matching (case-insensitively) {}.'.format(path + ext))
