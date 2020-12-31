#!/usr/bin/env python

# lib
import argparse
import xml.etree.ElementTree as ET

# local
import splitsutil
import timeutil

def variance(args):
    display_format = "{:<15}{:<15}{}"
    tree = ET.parse(args.splits_file)
    root = tree.getroot()
    segments = splitsutil.getSegmentsRoot(root)
    sortedByVariance = splitsutil.getVarianceSorted(segments, minAttemptId=args.minattemptid)
    print(display_format.format("Mean Time", "Variance", "Split Name"))
    for mean, variance, name in sortedByVariance:
        mean_time = timeutil.fromMilliseconds(mean)
        mean_display = timeutil.formatTimeTuple(mean_time)
        display = display_format.format(mean_display, variance, name)
        print(display)

def createParser():
    parser = argparse.ArgumentParser(description='Analyze .lss Splits Files')
    subparsers = parser.add_subparsers()
    parser_variance = subparsers.add_parser('variance')
    parser_variance.set_defaults(func=variance)
    parser_variance.add_argument('splits_file', type=str, help='The .lss splits file to analyze')
    parser_variance.add_argument('--comparison', type=str, help='Time comparison to analyze. Defaults to GameTime',
                        default='GameTime', choices=['GameTime', 'RealTime'])
    parser_variance.add_argument('--minattemptid', type=int, help='Minimum attempt id to analyze. Drops data from attempts below this id.')
    return parser

def main():
    parser = createParser()
    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
