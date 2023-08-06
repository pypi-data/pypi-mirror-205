import argparse


SLICE_EPILOG = """
TIME ARGUMENT COMBINATION
    The --end and --duration arguments cannot be used together.
    Allowed combinations:
        --start, [ --frame-rate ]
        --start, --end, [ --frame-rate ]
        --start, --duration, [ --frame-rate ]

TIME FORMAT
    The time format for --start, --end, and --duration is as follows:
        ss[.ms]
        mm:ss[.ms]
        hh:mm:ss[.ms]
    where:
        ms: milliseconds (0 <= ms < 999)
        ss: seconds (0 <= ss < 59)
        mm: minutes (0 <= mm < 59)
        hh: hours (0 <= hh < infinity)
    Prefix zeros are allowed. For example, 00:00:07.120 is the same as 7.12
    If --frame-rate is specified, the time format works different.
    See FRAME RATE section for more details.

FRAME RATE
    When --frame-rate is specified, the time format for --start, --end, and --duration is as follows:
        ss[:ff]
        mm:ss[:ff]
        hh:mm:ss[:ff]
    where:
        ss, mm, hh: same as above
        ff: frame number (0 <= ff < frame rate)
    EXAMPLE: if frame rate is 60, ff = 120 stands for 00:02:00.000

EXAMPLES
    Slice from 00:04:12 to 00:07:12:
        danmakuctl slice --start 00:04:12 --end 00:07:12 input.xml output.xml
    Or, use duration:
        danmakuctl slice --start 00:04:12 --duration 00:03:00 input.xml output.xml
    
    Slice from 00:07:12 to end:
        danmakuctl slice --start 00:07:12 input.xml output.xml
    
    Suppose frame rate is 60, slice from the 30th from of 00:04:12 to the 15th frame of 00:07:12:
        danmakuctl slice --start 00:04:12:30 --end 00:07:12:15 --frame-rate 60 input.xml output.xml
    Or, use milliseconds:
        danmakuctl slice --start 00:04:12.5 --end 00:07:12.25 input.xml output.xml
"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='merge & split danmaku BiliBili XML files')
    subparsers = parser.add_subparsers(dest='command')

    # Sub-command "analyze"
    parser_analyze = subparsers.add_parser('analyze', help='Analyze danmaku file')
    parser_analyze.add_argument('danmaku', type=str, help='path to the danmaku file')
    parser_analyze.add_argument('--income', action="store_true", help='show income', default=False)

    # Sub-command "merge"
    parser_merge = subparsers.add_parser('merge', help='Merge multiple danmaku files into one')
    parser_merge.add_argument('input', type=str, nargs='+', help='input danmaku files')
    parser_merge.add_argument('output', type=str, help='output merged danmaku file')

    # Sub-command "slice"
    parser_slice = subparsers.add_parser('slice', help='Split danmaku file into multiple files', epilog=SLICE_EPILOG, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser_slice.add_argument('input', type=str, help='input danmaku file')
    parser_slice.add_argument('output', type=str, help='output sliced danmaku file')
    parser_slice.add_argument('-s', '--start', type=str, help='start time of slice', default="0")
    parser_slice.add_argument('-e', '--end', type=str, help='end time of slice', default=None)
    parser_slice.add_argument('-t', '--duration', type=str, help='duration of slice', default=None)
    parser_slice.add_argument('-i', '--frame-rate', type=int, help='frame rate of video', default=None)

    return parser.parse_args()


def main():
    args = parse_args()
    if args.command == 'analyze':
        from bilibili_danmaku_tools.analyze import analyze
        return analyze(
            danmaku_file=args.danmaku,
            income=args.income,
        )
    if args.command == 'slice':
        from bilibili_danmaku_tools.slice import slice
        return slice(
            input=args.input,
            output=args.output,
            start=args.start,
            end=args.end,
            duration=args.duration,
            frame_rate=args.frame_rate,
        )
    if args.command == 'merge':
        from bilibili_danmaku_tools.merge import merge
        return merge(
            inputs=args.input,
            output=args.output,
        )
    print("No command specified. Run with --help for help.")
    return
