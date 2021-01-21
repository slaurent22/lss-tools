from argparse import Namespace
from typing import Dict, Tuple
from .splits import Splits
from .timeutil import format_from_milliseconds, format_time_tuple, to_milliseconds, TimeTuple


TimeDict = Dict[int, TimeTuple]
CombinedTimeEntry = Tuple[int, int, int]
CombinedTimeDict = Dict[int, CombinedTimeEntry]


def display_time_dict(time_dict: TimeDict):
    for entry in time_dict.items():
        time_id, time_tuple = entry
        print(time_id, format_time_tuple(time_tuple))


def _combined_time_sort_key_(combined_entry: Tuple[int, CombinedTimeEntry]):
    _, times = combined_entry
    _, _, time_sum = times
    return time_sum


def display_combined_time_dict(combined_dict: CombinedTimeDict, time_a_label: str, time_b_label: str):
    format_str = '{:<15}{:<20}{:<20}{:<15}'
    print(format_str.format('Attempt id', time_a_label, time_b_label, 'Sum'))
    combined_dict_items_sorted = sorted(combined_dict.items(), key=_combined_time_sort_key_)
    for entry in combined_dict_items_sorted:
        time_id, times = entry
        time_a, time_b, time_sum = times
        display = format_str.format(time_id,
                                    format_from_milliseconds(time_a),
                                    format_from_milliseconds(time_b),
                                    format_from_milliseconds(time_sum))
        print(display)


def __combine_time_dicts_helper__(combined, time_dict_a, time_dict_b, invert=False):
    for item in time_dict_a.items():
        time_id, time_tuple_a = item
        time_tuple_b = None
        if time_id in time_dict_b:
            time_tuple_b = time_dict_b[time_id]
        time_a, time_b = to_milliseconds(time_tuple_a), to_milliseconds(time_tuple_b)
        time_sum = time_a + time_b
        combined_entry = (time_b, time_a, time_sum) if invert else (time_a, time_b, time_sum)
        combined[time_id] = combined_entry


def combine_time_dicts(time_dict_a: TimeDict, time_dict_b: TimeDict):
    combined: CombinedTimeDict = {}
    __combine_time_dicts_helper__(combined, time_dict_a, time_dict_b)
    __combine_time_dicts_helper__(combined, time_dict_b, time_dict_a, invert=True)
    return combined


def merge(splits: Splits, args: Namespace):
    print('Merging on "{}"'.format(args.merge_point))
    segments = list(splits.segments)
    merge_segment_match = [(index, seg) for (index, seg) in enumerate(segments) if seg.name == args.merge_point]
    if len(merge_segment_match) != 1:
        print('Expected to find 1 matching segment, found {} instead'.format(len(merge_segment_match)))
        return
    (merge_segment_index, merge_segment) = merge_segment_match[0]
    next_segment = segments[merge_segment_index + 1]
    print('Merging into "{}"'.format(next_segment.name))
    print('Sorting by merged Golds. The top time is the proper combined gold, from a single run')
    print()

    merge_segment_time_dict: Dict[int, TimeTuple] = merge_segment.get_game_time_dict()
    next_segment_time_dict: Dict[int, TimeTuple] = next_segment.get_game_time_dict()

    combined = combine_time_dicts(merge_segment_time_dict, next_segment_time_dict)
    display_combined_time_dict(combined, args.merge_point, next_segment.name)

    # display_time_dict(merge_segment_time_dict)
    # display_time_dict(next_segment_time_dict)
