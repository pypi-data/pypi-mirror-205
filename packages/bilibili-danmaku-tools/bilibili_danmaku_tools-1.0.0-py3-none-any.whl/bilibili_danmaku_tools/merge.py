import xml.etree.ElementTree as ET
from typing import Optional
from datetime import datetime
from bilibili_danmaku_tools.defs import SYSTEM_NODE_NAMES, WELL_KNOWN_NODE_NAMES


def timecode_handler_ts(node: ET.Element, offset: float) -> Optional[ET.Element]:
    node_time = float(node.attrib['ts'])
    offseted_time = round(node_time + offset, 3)
    node.set('ts', str(offseted_time))
    return node


def timecode_handler_danmaku(node: ET.Element, offset: float) -> Optional[ET.Element]:
    node_parameters = node.attrib['p'].split(',')
    node_time = float(node_parameters[0])
    offseted_time = round(node_time + offset, 3)
    new_parameters = [str(offseted_time)] + node_parameters[1:]
    node.set('p', ','.join(new_parameters))
    return node


def merge_xml(root: ET.Element, merging_root: ET.Element, offset: float):
    for node in merging_root:
        if node.tag in [i["nodename"] for i in filter(lambda x: x["timecoder"] == "ts", WELL_KNOWN_NODE_NAMES)]:
            result_node = timecode_handler_ts(node, offset)
            if result_node is not None:
                root.append(result_node)
            continue
        if node.tag in [i["nodename"] for i in filter(lambda x: x["timecoder"] == "danmaku", WELL_KNOWN_NODE_NAMES)]:
            result_node = timecode_handler_danmaku(node, offset)
            if result_node is not None:
                root.append(result_node)
            continue
        if node.tag in SYSTEM_NODE_NAMES:
            continue
        if node.tag.startswith("BililiveRecorder"):
            continue
        root.append(node)


def merge(inputs: list[str], output: str):
    tree = ET.parse(inputs[0])
    root = tree.getroot()
    base = datetime.fromisoformat(root.findall('BililiveRecorderRecordInfo')[0].attrib['start_time'])
    print(f"Base time: {base} (file: {inputs[0]})")

    merging_xmls = [{ "file": file } for file in inputs]
    for merging_xml in merging_xmls:
        merging_xml['root'] = ET.parse(merging_xml['file']).getroot()
        merging_xml['base'] = datetime.fromisoformat(merging_xml['root'].findall('BililiveRecorderRecordInfo')[0].attrib['start_time'])
        merging_xml['offset'] = merging_xml['base'].timestamp() - base.timestamp()
    max_offset_length = max([len(str(int(merging_xml['offset']))) for merging_xml in merging_xmls]) + 3 + 1

    for merging_xml in merging_xmls:
        info = ET.Element('bilibili-danmaku-tools-merge-info')
        info.set('file', merging_xml['file'])
        info.set('start_time', str(merging_xml['base']))
        info.set('offset', str(merging_xml['offset']))
        root.append(info)
    
    for merging_xml in merging_xmls[1:]:
        formatter = "Next time: {base} (offset: {offset:>" + str(max_offset_length) + ".3f}, file: {file})"
        print(formatter.format(base=merging_xml['base'], offset=merging_xml['offset'], file=merging_xml['file']))
        root.append(ET.Comment(f"File: {merging_xml['file']}"))
        merge_xml(root, merging_xml['root'], merging_xml['offset'])

    tree.write(output, encoding="utf-8", xml_declaration=True)
