"""Parse all traits for the input record."""

from traiter_vertnet.parsers.as_is import AS_IS


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


class RecordParser:  # pylint: disable=too-few-public-methods
    """Handles all of the parsed traits for a record."""

    as_is = AS_IS

    def __init__(self, parsers, search_fields=None, as_is_fields=None):
        """Create the record container."""
        self.parsers = parsers
        self.search_fields = search_fields if search_fields else []
        self.as_is_fields = as_is_fields if as_is_fields else {}

    def parse_record(self, record):
        """Parse the traits for record."""
        data = {trait: [] for trait, parser in self.parsers}

        for trait, parser in self.parsers:
            try:

                if parser.should_skip(data, trait):
                    raise ShouldSkip()

                for field in self.as_is_fields.get(trait, []):
                    parsed = self.as_is.parse(record[field], field)
                    if parsed:
                        data[trait] += parsed
                        raise TraitFound()

                for field in self.search_fields:
                    parsed = parser.parse(record[field], field)
                    if parsed:
                        data[trait] += parsed
                        raise TraitFound()

            except TraitFound:
                parser.adjust_record(data, trait)

            except ShouldSkip:
                pass

        return data