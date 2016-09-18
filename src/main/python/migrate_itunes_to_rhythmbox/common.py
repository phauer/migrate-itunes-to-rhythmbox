from lxml import etree
from path import Path


def write_to_file(root, target_path: Path):
    xml_string = etree.tostring(root, pretty_print=True, xml_declaration=True, encoding='UTF-8')
    final_string = xml_string.decode('UTF-8')
    with target_path.open("w") as output_file:
        print(final_string, file=output_file)