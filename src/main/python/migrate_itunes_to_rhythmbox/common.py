from lxml import etree
from path import Path


def get_xml_declaration(add_standalone_to_xml_declaration: bool):
    if add_standalone_to_xml_declaration:
        return "<?xml version=\"1.0\" standalone=\"yes\"?>\n"
    else:
        return "<?xml version=\"1.0\"?>\n"


def write_to_file(root, target_path: Path, add_standalone_to_xml_declaration: bool = False):
    xml_string = etree.tostring(root, pretty_print=True, xml_declaration=False)  # stick to rhythmbox' xml_declaration (double quotes, no encoding, maybe standalone)
    xml_declaration = get_xml_declaration(add_standalone_to_xml_declaration)
    final_string = xml_declaration + xml_string.decode('UTF-8')
    with target_path.open("w") as output_file:
        print(final_string, file=output_file)