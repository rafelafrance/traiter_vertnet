"""Parse all traits for the input record."""

# from vertnet.parsers.as_is import AS_IS


class TraitFound(Exception):
    """
    Stop looking for parses because we found one.

    If one field has a trait notation (or multiple) then don't look for the
    trait in other fields.
    """


class ShouldSkip(Exception):
    """
    Don't parse the trait because of another condition.

    For instance, don't look for testes traits on females.
    """


class RecordParser:
    """Handles all of the parsed traits for a record."""

    def __init__(self, args, parsers):
        """Create the record container."""
        self.parsers = parsers
        self.search_fields = args.search_field if args.search_field else []

    def parse_record(self, record):
        """Parse the traits for record."""
        print(record)
        data = {}

        something_found = False
        for trait, parser in self.parsers:
            try:
                for field_name in self.search_fields:
                    field = record.get(field_name)
                    if not field:
                        continue
                    parsed = parser.parse(field, field_name)
                    if parsed:
                        data[trait] = parsed
                        something_found = True
                        raise TraitFound()
            except TraitFound:
                pass

        return data if something_found else None
