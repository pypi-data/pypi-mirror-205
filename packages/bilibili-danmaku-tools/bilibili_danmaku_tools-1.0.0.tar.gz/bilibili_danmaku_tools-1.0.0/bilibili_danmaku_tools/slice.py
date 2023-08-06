import xml.etree.ElementTree as ET
from typing import Optional
from datetime import datetime, timedelta
from bilibili_danmaku_tools.defs import WELL_KNOWN_NODE_NAMES


def parse_time(expression: str, frame_rate: Optional[int] = None) -> float:
    if frame_rate is not None:
        hms = expression.split(':')[:-1]
        ms = float(int(expression.split(':')[-1]) / frame_rate)
    elif '.' in expression:
        hms = expression.split('.')[0].split(':')
        ms = float("0." + expression.split('.')[1])
    else:
        hms = expression.split(':')
        ms = float(0)
    
    if len(hms) == 3:
        h, m, s = hms
    elif len(hms) == 2:
        m, s = hms
    elif len(hms) == 1:
        s = hms[0]
        h = 0
        m = 0
    else:
        raise ValueError(f"Invalid hh:mm:ss part of time expression: {expression}")
    h, m, s = int(h), int(m), int(s)
    return h * 3600 + m * 60 + s + ms


def prase_time_expression(start: str, end: Optional[str], duration: Optional[str], frame_rate: Optional[int] = None) -> tuple[float, float]:
    if (end is not None) and (duration is not None):
        raise ValueError("Cannot specify both end and duration")
    start_second = parse_time(start, frame_rate)
    if end is not None:
        end_second = parse_time(end, frame_rate)
    else:
        end_second = start_second + parse_time(duration, frame_rate)
    return start_second, end_second


def timecode_handler_ts(node: ET.Element, start_time: float, end_time: float) -> Optional[ET.Element]:
    node_time = float(node.attrib['ts'])
    if start_time <= node_time <= end_time:
        new_time = node_time - start_time
        new_time = round(new_time, 3)
        new_time_str = str(new_time)
        node.set('ts', new_time_str)
        return node
    return None


def timecode_handler_danmaku(node: ET.Element, start_time: float, end_time: float) -> Optional[ET.Element]:
    node_parameters = node.attrib['p'].split(',')
    node_time = float(node_parameters[0])
    if start_time <= node_time <= end_time:
        new_time = node_time - start_time
        new_time = round(new_time, 3)
        new_parameters = [str(new_time)] + node_parameters[1:]
        node.set('p', ','.join(new_parameters))
        return node
    return None


def process_nodes(root, start_time, end_time):
    result = ET.Element('i')
    for node in root:
        if node.tag in [i["nodename"] for i in filter(lambda x: x["timecoder"] == "ts", WELL_KNOWN_NODE_NAMES)]:
            result_node = timecode_handler_ts(node, start_time, end_time)
            if result_node is not None:
                result.append(result_node)
            continue
        if node.tag in [i["nodename"] for i in filter(lambda x: x["timecoder"] == "danmaku", WELL_KNOWN_NODE_NAMES)]:
            result_node = timecode_handler_danmaku(node, start_time, end_time)
            if result_node is not None:
                result.append(result_node)
            continue
        if node.tag in ['BililiveRecorderRecordInfo']:
            record_at = node.attrib['start_time']
            slice_start_iso_time = datetime.fromisoformat(node.attrib['start_time']) + timedelta(seconds=start_time)
            slice_end_iso_time = datetime.fromisoformat(node.attrib['start_time']) + timedelta(seconds=end_time)
            node.set('start_time', slice_start_iso_time.isoformat())
            node.set('end_time', slice_end_iso_time.isoformat())
            node.set('record_at', record_at)
            result.append(node)
            continue
        result.append(node)
    return result



def slice(input: str, output: str, start: str, end: Optional[str] = None, duration: Optional[str] = None, frame_rate: Optional[int] = None):
    start_second, end_second = prase_time_expression(start, end, duration, frame_rate)
    xml = ET.parse(input)
    root = xml.getroot()
    result = process_nodes(root, start_second, end_second)
    ET.ElementTree(result).write(output, encoding='UTF-8', xml_declaration=True)
