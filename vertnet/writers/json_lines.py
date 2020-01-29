"""Write the output to a JSON Lines file."""

import json
from vertnet.writers.base_writer import BaseWriter


class JsonLinesWriter(BaseWriter):
    """Write the lib output to a file."""

    def __init__(self, args):
        """Build the writer."""
        super().__init__(args)
        self.columns = args.extra_field
        self.columns += args.search_field

    def start(self):
        """Start the report."""

    def record(self, raw_record, parsed_record):
        """Output a row to the file."""
        row = {**raw_record, **parsed_record}
        obj = json.dumps(row) + '\n'
        self.args.output_file.write(obj)

    def end(self):
        """End the report."""

