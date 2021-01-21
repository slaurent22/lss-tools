from datetime import datetime
from typing import Tuple

MS_PER_SECOND = 1000
MS_PER_MINUTE = 60 * MS_PER_SECOND
MS_PER_HOUR = 60 * MS_PER_MINUTE
MICROSENDS_PER_MILLLISECOND = 1000

STD_FORMAT_LENGTH = len('00:01:11.1150000')
NO_PRECISION_FORMAT_LENGTH = len('00:01:18')

# hour, minute, second, milliseconds
TimeTuple = Tuple[int, int, int, int]


def __qrem__(a: int, b: int) -> Tuple[int, int]:
    return a // b, a % b


def parse_time(time_text: str) -> TimeTuple:
    # TODO: This is a super hack. Figure out a cleaner way of accounting for both formats
    to_parse = time_text
    format_string = "%H:%M:%S.%f"
    if len(time_text) == STD_FORMAT_LENGTH:
        to_parse = time_text[0:len(time_text) - 1]
    elif len(time_text) == NO_PRECISION_FORMAT_LENGTH:
        format_string = "%H:%M:%S"
    parsed = datetime.strptime(to_parse, format_string)
    return parsed.hour, parsed.minute, parsed.second, int(parsed.microsecond / MICROSENDS_PER_MILLLISECOND)


def to_milliseconds(time_tuple: TimeTuple) -> int:
    hour, minute, second, millisecond = time_tuple
    return hour * MS_PER_HOUR + minute * MS_PER_MINUTE + second * MS_PER_SECOND + millisecond


def from_milliseconds(ms: int) -> TimeTuple:
    ms_left = ms
    hour, ms_left = __qrem__(ms_left, MS_PER_HOUR)
    minute, ms_left = __qrem__(ms_left, MS_PER_MINUTE)
    second, ms_left = __qrem__(ms_left, MS_PER_SECOND)
    return hour, minute, second, ms_left


def format_time_tuple(time_tuple: TimeTuple) -> str:
    hour, minute, second, millisecond = time_tuple
    return "{:02d}:{:02d}:{:02d}.{:03d}".format(hour, minute, second, millisecond)


def format_from_milliseconds(ms: int) -> str:
    return format_time_tuple(from_milliseconds(ms))
