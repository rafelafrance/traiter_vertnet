"""Write the output to a JSON Lines file."""

import json
from vertnet.writers.base_writer import BaseWriter


class JsonLinesWriter(BaseWriter):  # pylint: disable=too-few-public-methods
    """Write the lib output to a file."""

    def __init__(self, args):
        """Build the writer."""
        super().__init__(args)
        self.columns = args.extra_field
        self.columns += args.search_field

    def write(self, raw_record, parsed_record):
        """Output a row to the file."""
        if not parsed_record:
            return
        raw_record = {k: v for k, v in raw_record.items() if v}
        row = {**raw_record, **parsed_record}
        obj = json.dumps(row) + '\n'
        self.args.output_file.write(obj)
