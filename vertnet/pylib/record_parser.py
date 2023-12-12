"""Parse all traits for the input record."""
from collections import defaultdict


class RecordParser:  # pylint: disable=too-few-public-methods
    """Handles all the parsed traits for a record."""

    def __init__(self, args, parsers):
        """Create the record container."""
        self.parsers = parsers
        self.search_fields = args.search_field if args.search_field else []

    def parse_record(self, record):
        """Parse the traits for record."""
        data = defaultdict(list)

        for trait, parser in self.parsers:
            for field_name in self.search_fields:
                field = record.get(field_name)
                if not field:
                    continue
                parsed = parser.parse(field, field_name)
                if parsed:
                    data[trait] += parsed

        return data
