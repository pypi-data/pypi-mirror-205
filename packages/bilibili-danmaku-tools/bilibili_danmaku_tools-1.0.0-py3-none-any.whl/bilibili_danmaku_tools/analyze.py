import xml.etree.ElementTree as ET
import bilibili_danmaku_tools.defs as defs
import bilibili_danmaku_tools.danmaku_xml as danmaku_xml


WELL_KNOWN_NODE_NAMES = {i['nodename']: i['display_name'] for i in defs.WELL_KNOWN_NODE_NAMES}


def anaylzer_common(node: ET.Element, counter: dict[str, int]) -> dict[str, int]:
    if node.tag in defs.SYSTEM_NODE_NAMES:
        return counter
    if node.tag.startswith('BililiveRecorder'):
        return counter
    counter[node.tag] = counter.get(node.tag, 0) + 1
    return counter


def anaylzer_income(node: ET.Element, counter: dict[str, int]) -> dict[str, int]:
    if node.tag == 'sc':
        counter["sc"] = counter.get("sc", 0) + int(node.attrib['price'])
    return counter


def report_analyze(danmaku_file: str, anaylzer: callable):
    danmaku = danmaku_xml.load(danmaku_file)
    counter = {}
    for node in danmaku:
        counter = anaylzer(node, counter)
    number_max_length = max(max([len(str(i)) for i in counter.values()]), 6) + 1
    nodename_max_length = max(max([len(str(i)) for i in counter.keys()]), 6) + 1
    total = sum(counter.values())
    formatter = "{nodename:<" + str(nodename_max_length) + "}  {number:>" + str(number_max_length) + "}  {percentage:>7.2%}  # {comment}"
    for nodename, number in counter.items():
        print(formatter.format(
            nodename=nodename,
            number=number,
            percentage=number / total,
            comment=WELL_KNOWN_NODE_NAMES.get(nodename, "未知"),
        ))
    print(formatter.format(
        nodename="_total",
        number=total,
        percentage=1,
        comment="总计",
    ))


def analyze(danmaku_file: str, income: bool = False):
    report_analyze(danmaku_file, anaylzer_common)
    if income:
        print("-" * 60)
        print("收入统计")
        report_analyze(danmaku_file, anaylzer_income)
