from typing import NamedTuple

from .util import DotDict, as_list, squash


class TraitKey(NamedTuple):
    value: str
    side: str


class Trait(DotDict):  #
    def transfer(self, token, names):
        """Move fields from a token to the trait if they exist in the token."""
        for name in names:
            if name in token.group:
                values = [v.lower() for v in as_list(token.group[name])]
                setattr(self, name, squash(values))

    def is_flag_in_token(self, token, flag, rename=None):
        """Set a flag if it is found in the token's groups field."""
        if token.group.get(flag):
            flag = rename if rename else flag
            setattr(self, flag, True)

    def is_flag_missing(self, token, flag, rename=None):
        """Set a flag if it is found in the token's groups field."""
        if not token.group.get(flag):
            flag = rename if rename else flag
            setattr(self, flag, True)

    def is_value_in_token(self, token, flag, rename=None):
        """Set a flag if it is found in the token's groups field."""
        if value := token.group.get(flag):
            flag = rename if rename else flag
            setattr(self, flag, value.lower())

    def merge_ambiguous_key(self, other):
        """Capture the meaning across all parses."""
        ambiguous_key = bool(self.ambiguous_key)
        ambiguous_key &= bool(other.ambiguous_key)
        self.ambiguous_key = ambiguous_key

    def as_key(self):
        """Determine if the traits are the same trait."""
        return TraitKey(value=self.value, side=self.side)
