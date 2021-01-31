"""Write the output to a CSV file."""

import regex
import pandas as pd
from vertnet.writers.base_writer import BaseWriter


class CsvWriter(BaseWriter):
    """Write the lib output to a file."""

    def __init__(self, args):
        """Build the writer."""
        super().__init__(args)
        self.columns = args.extra_field
        self.columns += args.search_field
        self.columns += sorted({f for fds in args.as_is.values() for f in fds})

    def __enter__(self):
        """Start the report."""
        self.rows = []

    def __exit__(self, exc_type, exc_value, traceback):
        """End the report."""
        dfm = pd.DataFrame(self.rows)
        dfm.rename(
            columns=lambda x: regex.sub(r'^.+?:\s*', '', x), inplace=True)
        dfm.to_csv(self.args.output_file, index=False)

    def write(self, raw_record, parsed_record):
        """Output a record to the file."""
        row = {c: raw_record.get(c, '') for c in self.columns}

        self.rows.append(row)
