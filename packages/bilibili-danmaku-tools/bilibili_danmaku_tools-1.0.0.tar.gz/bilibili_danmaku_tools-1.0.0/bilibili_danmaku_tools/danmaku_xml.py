import xml.etree.ElementTree as ET
import json


def load(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    return [node for node in root]


def get_time(child: ET.Element):
    # noinspection PyBroadException
    try:
        if child.tag == 'd':
            return float(child.attrib['p'].split(',')[0])
        elif child.tag == 'gift' or child.tag == 'sc':
            return float(child.attrib['ts'])
    except:
        print(f"error getting time from {child}")
        return 0
