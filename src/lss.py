#!/usr/bin/env python

# lib
import argparse
import xml.etree.ElementTree as ET

# local
import splitsutil
import timeutil


def deviation(args):
    display_format = "{:<15}{:<15}{:<15}{:<15}{}"
    tree = ET.parse(args.splits_file)
    root = tree.getroot()
    segments = splitsutil.getSegmentsRoot(root)
    sortedByDeviation = splitsutil.getDeviationSorted(
        segments, minAttemptId=args.minattemptid, comparison=args.comparison)
    print(display_format.format("Mean", "Median", "Deviation", "Gold", "Split Name"))
    for mean, deviation, name, median, gold in sortedByDeviation:
        mean_display = timeutil.formatFromMilliseconds(mean)
        deviation_display = timeutil.formatFromMilliseconds(deviation)
        median_display = timeutil.formatFromMilliseconds(median)
        gold_display = timeutil.formatFromMilliseconds(gold)
        display = display_format.format(mean_display, median_display, deviation_display, gold_display, name)
        print(display)


def createParser():
    parser = argparse.ArgumentParser(description='Analyze .lss Splits Files')
    subparsers = parser.add_subparsers()
    parser_deviation = subparsers.add_parser('deviation')
    parser_deviation.set_defaults(func=deviation)
    parser_deviation.add_argument('splits_file', type=str, help='The .lss splits file to analyze')
    parser_deviation.add_argument('--comparison', type=str, help='Time comparison to analyze. Defaults to GameTime',
                                  default='GameTime', choices=['GameTime', 'RealTime'])
    parser_deviation.add_argument('--minattemptid', type=int,
                                  help='Minimum attempt id to analyze. Drops data from attempts below this id.')
    return parser


def main():
    parser = createParser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
