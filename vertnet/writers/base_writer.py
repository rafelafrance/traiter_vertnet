"""Write the lib output to a file."""

from abc import abstractmethod
from contextlib import AbstractContextManager


class BaseWriter(AbstractContextManager):
    """Write the output to a file."""

    def __init__(self, args):
        """Build the writer."""
        self.args = args
        self.output_file = args.output_file
        self.rows = []

    def __enter__(self):
        """Use the writer in with statements."""
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Use the writer in with statements."""

    @abstractmethod
    def write(self, raw_record, parsed_record):
        """Output a report record."""
        raise NotImplementedError("You need a record function.")
