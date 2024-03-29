"""Read the lib input from a file."""

from abc import abstractmethod
from collections.abc import Iterable
from contextlib import AbstractContextManager


# pylint: disable=too-few-public-methods
class BaseReader(AbstractContextManager, Iterable):
    """Read the lib input from a file."""

    def __init__(self, args):
        """Build the reader."""
        self.args = args
        self.index = 0

    @abstractmethod
    def __iter__(self):
        """Iterate thru the input file."""
