# local
import timeutil


def __deviation_key__(segment_summary):
    return segment_summary['stats']['deviation']


def deviation(splits, args):
    display_format = "{:<15}{:<15}{:<15}{:<15}{}"
    summaries = splits.get_segment_summaries(min_attempt_id=args.minattemptid,
                                             comparison=args.comparison,
                                             zscore_cutoff=args.zscore_cutoff)

    summaries_by_deviation = sorted(summaries, reverse=True, key=__deviation_key__)
    print(display_format.format("Mean", "Median", "Deviation", "Gold", "Split Name"))
    for deviation_summary in summaries_by_deviation:
        gold = deviation_summary['gold']
        name = deviation_summary['name']
        stats = deviation_summary['stats']
        mean = stats['mean']
        median = stats['median']
        deviation = stats['deviation']
        mean_display = timeutil.format_from_milliseconds(mean)
        deviation_display = timeutil.format_from_milliseconds(deviation)
        median_display = timeutil.format_from_milliseconds(median)
        gold_display = timeutil.format_from_milliseconds(gold)
        display = display_format.format(mean_display, median_display, deviation_display, gold_display, name)
        print(display)
