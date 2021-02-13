from argparse import Namespace
from . import timeutil
from .splits import Splits


def __deviation_key__(segment_summary):
    return segment_summary['stats']['deviation']


def zscore_display_with_warning(gold_zscore, zscore_cutoff=None):
    if type(zscore_cutoff) is int:
        if abs(gold_zscore) > zscore_cutoff:
            return "{:<5}{:<4}".format(str(gold_zscore), " !!!")
    return "{:<5}".format(str(gold_zscore))


def deviation(splits: Splits, args: Namespace):
    display_format = "{:<15}{:<15}{:<15}{:<15}{:<15}{}"
    summaries = splits.get_segment_summaries(min_attempt_id=args.minattemptid,
                                             comparison=args.comparison,
                                             zscore_cutoff=args.zscore_cutoff,
                                             last_runs=args.last_runs)

    summaries_by_deviation = sorted(summaries, reverse=True, key=__deviation_key__)
    print(display_format.format("Mean", "Median", "Deviation", "Gold", "Gold Z-Score", "Split Name"))
    for deviation_summary in summaries_by_deviation:
        gold = deviation_summary['gold']
        gold_zscore = deviation_summary['gold_zscore']
        name = deviation_summary['name']
        stats = deviation_summary['stats']
        mean = stats['mean']
        median = stats['median']
        deviation = stats['deviation']
        mean_display = timeutil.format_from_milliseconds(mean)
        deviation_display = timeutil.format_from_milliseconds(deviation)
        median_display = timeutil.format_from_milliseconds(median)
        gold_display = timeutil.format_from_milliseconds(gold)
        gold_zscore_display = zscore_display_with_warning(gold_zscore, zscore_cutoff=args.zscore_cutoff)
        display = display_format.format(mean_display, median_display, deviation_display,
                                        gold_display, gold_zscore_display, name)
        print(display)
