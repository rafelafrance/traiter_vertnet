#!/usr/bin/env python3

"""Given a CSV file of natural history notes, parse parsers."""

import sys
import argparse
import textwrap
from vertnet.pylib.all_traits import TRAITS
from vertnet.pylib.record_parser import RecordParser
from vertnet.readers.csv_reader import CsvReader
from vertnet.writers.csv_writer import CsvWriter
from vertnet.writers.html_writer import HtmlWriter
from vertnet.writers.json_lines import JsonLinesWriter


__VERSION__ = '0.6.0'


INPUT_FORMATS = {
    'csv': CsvReader}

OUTPUT_FORMATS = {
    'csv': CsvWriter,
    'html': HtmlWriter,
    'jsonl': JsonLinesWriter}


def parse_traits(args):
    """Parse the input."""
    trait_parsers = [(trait, parser)
                     for trait, parser in TRAITS.items()
                     if trait in args.trait]

    reader = INPUT_FORMATS[args.input_format](args)
    writer = OUTPUT_FORMATS[args.output_format](args)

    record_parser = RecordParser(args, trait_parsers)

    with reader as input_file, writer as output_file:

        for record in input_file:
            record = {k: v for k, v in record.items()}

            parsed_record = record_parser.parse_record(record)

            if parsed_record:
                output_file.record(record, parsed_record)


def parse_args():
    """Process command-line arguments."""
    description = """Extract parsers from the file."""
    arg_parser = argparse.ArgumentParser(
        allow_abbrev=True,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent(description),
        fromfile_prefix_chars='@')

    arg_parser.add_argument(
        '--version', '-V', action='version',
        version='%(prog)s v{}'.format(__VERSION__))

    arg_parser.add_argument(
        '--input-file', '-i', type=argparse.FileType('r'), default=sys.stdin,
        help="""The input file containing the raw data. Defaults to stdin.""")

    arg_parser.add_argument(
        '--output-file', '-o', type=argparse.FileType('w'), default=sys.stdout,
        help="""Output the results to this file. Defaults to stdout.""")

    arg_parser.add_argument(
        '--trait', '-t', required=True, action='append',
        choices=TRAITS.keys(),
        help="""A trait to extract.""")

    arg_parser.add_argument(
        '--search-field', '-s', action='append', metavar='FIELD',
        help=f"""A field that contains the data to parse.
            You may use this argument more than once.""")

    arg_parser.add_argument(
        '--extra-field', '-e', action='append', metavar='FIELD',
        help="""An extra field to to append to an output row. You may use this
            argument more than once.""")

    arg_parser.add_argument(
        '--input-format', '-I', default='csv', choices=INPUT_FORMATS.keys(),
        help="""The data input format. The default is "csv".""")

    arg_parser.add_argument(
        '--output-format', '-O', default='jsonl',
        choices=OUTPUT_FORMATS.keys(),
        help="""Output the result in this format. The default is "jsonl".""")

    args = arg_parser.parse_args()

    return args


if __name__ == "__main__":
    ARGS = parse_args()
    parse_traits(ARGS)