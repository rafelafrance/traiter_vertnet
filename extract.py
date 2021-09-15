#!/usr/bin/env python3

"""Given a file of natural history notes, parse traits."""

import argparse
import sys
import textwrap
from pathlib import Path

from tqdm import tqdm

from vertnet.pylib.all_traits import TRAITS
from vertnet.pylib.record_parser import RecordParser
from vertnet.readers.csv_reader import CsvReader
from vertnet.writers.csv_writer import CsvWriter
from vertnet.writers.html_writer import HtmlWriter
from vertnet.writers.json_lines import JsonLinesWriter

INPUT_FORMATS = {"csv": CsvReader}

OUTPUT_FORMATS = {"csv": CsvWriter, "html": HtmlWriter, "jsonl": JsonLinesWriter}


def main(args):
    """Perform actions based on the arguments."""
    reader = INPUT_FORMATS[args.input_format](args)
    with reader as in_file:
        for row in in_file:
            print(row)
            break


def parse_traits(args):
    """Parse the input."""
    trait_parsers = [
        (trait, parser) for trait, parser in TRAITS.items() if trait in args.trait
    ]

    reader = INPUT_FORMATS[args.input_format](args)
    writer = OUTPUT_FORMATS[args.output_format](args)

    record_parser = RecordParser(args, trait_parsers)

    with reader as input_file, writer as output_file:

        for record in tqdm(input_file, disable=args.progress):
            record = dict(record.items())

            parsed_record = record_parser.parse_record(record)
            output_file.write(record, parsed_record)


def parse_args():
    """Process command-line arguments."""
    description = """Extract parsers from the file."""
    arg_parser = argparse.ArgumentParser(
        description=textwrap.dedent(description), fromfile_prefix_chars="@"
    )

    arg_parser.add_argument(
        "--input-file",
        type=Path,
        help="""The input file containing the raw data. Defaults to stdin.""",
    )

    arg_parser.add_argument(
        "--output-file",
        type=argparse.FileType("w"),
        default=sys.stdout,
        help="""Output the results to this file. Defaults to stdout.""",
    )

    arg_parser.add_argument(
        "--trait",
        required=True,
        action="append",
        choices=TRAITS.keys(),
        help="""A trait to extract.""",
    )

    arg_parser.add_argument(
        "--search-field",
        action="append",
        metavar="FIELD",
        help="""A field that contains the data to parse.
            You may use this argument more than once.""",
    )

    arg_parser.add_argument(
        "--extra-field",
        "-e",
        action="append",
        metavar="FIELD",
        help="""An extra field to to append to an output row. You may use this
            argument more than once.""",
    )

    arg_parser.add_argument(
        "--input-format",
        default="csv",
        choices=INPUT_FORMATS.keys(),
        help="""The data input format. The default is "csv".""",
    )

    arg_parser.add_argument(
        "--output-format",
        default="jsonl",
        choices=OUTPUT_FORMATS.keys(),
        help="""Output the result in this format. The default is "jsonl".""",
    )

    arg_parser.add_argument(
        "--progress", action="store_false", help="""Show a progress bar."""
    )

    args = arg_parser.parse_args()

    return args


if __name__ == "__main__":
    ARGS = parse_args()
    # main(ARGS)
    parse_traits(ARGS)
