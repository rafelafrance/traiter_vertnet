"""Read the lib input from a CSV file."""

import csv

from vertnet.readers.base_reader import BaseReader


class CsvReader(BaseReader):
    """Read the lib input from a file."""

    def __init__(self, args):
        """Build the reader."""
        super().__init__(args)
        self.reader = None
        self.input_file = args.input_file
        self.columns = args.search_field + args.extra_field

    def __enter__(self):
        """Use the reader in with statements."""
        self.handle = self.input_file.open()
        self.reader = csv.DictReader(self.handle)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Close the file handle."""
        self.handle.close()

    def __iter__(self):
        """Loop thru the file."""
        for row in self.reader:
            cols = {k: v for k, v in row.items() if k in self.columns}
            yield cols
