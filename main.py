#!/usr/bin/env python

import argparse
from lss.deviation import deviation
from lss.merge import merge
from lss.splits import Splits
import xml.etree.ElementTree as ET

DEFAULT_COMPARISON = 'GameTime'


def positive_int(value):
    ivalue = int(value)
    if ivalue <= 0:
        raise argparse.ArgumentTypeError('{} is an invalid positive int value'.format(value))
    return ivalue


def add_parser_deviation(subparsers):
    parser_deviation = subparsers.add_parser('deviation')
    parser_deviation.set_defaults(func=deviation)
    parser_deviation.add_argument('splits_file',
                                  type=str,
                                  help='The .lss splits file to analyze')
    parser_deviation.add_argument('--comparison',
                                  type=str,
                                  help='Time comparison to analyze. Default: {}'.format(DEFAULT_COMPARISON),
                                  default=DEFAULT_COMPARISON,
                                  choices=['GameTime', 'RealTime'])
    parser_deviation.add_argument('--minattemptid',
                                  type=int,
                                  help='Minimum attempt id to analyze. Drops data from attempts below this id.')
    parser_deviation.add_argument('--zscore-cutoff',
                                  type=positive_int,
                                  help='Z-Score outside of which to drop outliers.')
    parser_deviation.add_argument('--last-runs',
                                  type=positive_int,
                                  help='Analyzes the most recent X runs. Drops all data before these runs')
    
    return parser_deviation


def add_parser_merge(subparsers):
    parser_deviation = subparsers.add_parser('merge')
    parser_deviation.set_defaults(func=merge)
    parser_deviation.add_argument('splits_file',
                                  type=str,
                                  help='The .lss splits file to analyze')
    parser_deviation.add_argument('merge_point',
                                  type=str,
                                  help='The the name of the split to remove')


def create_parser():
    parser = argparse.ArgumentParser(description='Analyze .lss Splits Files')
    subparsers = parser.add_subparsers(dest='command')
    subparsers.required = True
    add_parser_deviation(subparsers)
    add_parser_merge(subparsers)
    return parser


def main():
    parser = create_parser()
    args = parser.parse_args()

    tree = ET.parse(args.splits_file)
    splits_xml_root = tree.getroot()
    splits = Splits(splits_xml_root)
    args.func(splits, args)


if __name__ == "__main__":
    main()
