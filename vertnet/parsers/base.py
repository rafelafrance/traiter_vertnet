from typing import Callable
from typing import List

from traiter.old.parser import Parser
from traiter.old.parser import RulesInput

from vertnet.pylib.trait import Trait


def fix_up_nop(trait, _):
    return trait


class Base(Parser):
    def __init__(
        self,
        rules: RulesInput,
        name: str = "parser",
        fix_up: Callable[[Trait, str], Trait] = None,
    ) -> None:
        """Build the trait parser."""
        super().__init__(name=name, rules=rules)
        self.fix_up = fix_up if fix_up else fix_up_nop

    # pylint: disable=arguments-differ
    def parse(self, text: str, field: str = None) -> List[Trait]:
        """Find the traits in the text."""
        traits = []

        tokens = super().parse(text)

        for token in tokens:

            trait_list = token.action(token)

            # The action function can reject the token
            if not trait_list:
                continue

            # Some parses represent multiple traits, fix them all up
            if not isinstance(trait_list, list):
                trait_list = [trait_list]

            # Add the traits after any fix up.
            for trait in trait_list:
                trait = self.fix_up(trait, text)
                if trait:  # The parse may fail during fix up
                    if field:
                        trait.field = field
                    traits.append(trait)

        # from pprint import pp
        # pp(traits)

        return traits


def convert(token):
    """Convert parsed tokens into a result."""
    return Trait(value=token.group["value"].lower(), start=token.start, end=token.end)
