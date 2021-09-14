"""All of the parsers."""

from vertnet.parsers.body_mass import BODY_MASS
from vertnet.parsers.ear_length import EAR_LENGTH
from vertnet.parsers.embryo_count import EMBRYO_COUNT
from vertnet.parsers.embryo_length import EMBRYO_LENGTH
from vertnet.parsers.forearm_length import FOREARM_LENGTH
from vertnet.parsers.hind_foot_length import HIND_FOOT_LENGTH
from vertnet.parsers.lactation_state import LACTATION_STATE
from vertnet.parsers.life_stage import LIFE_STAGE
from vertnet.parsers.nipple_count import NIPPLE_COUNT
from vertnet.parsers.nipple_state import NIPPLE_STATE
from vertnet.parsers.ovaries_size import OVARY_SIZE
from vertnet.parsers.ovaries_state import OVARIES_STATE
from vertnet.parsers.placental_scar_count import PLACENTAL_SCAR_COUNT
from vertnet.parsers.placental_scar_state import PLACENTAL_SCAR_STATE
from vertnet.parsers.pregnancy_state import PREGNANCY_STATE
from vertnet.parsers.scrotal_state import SCROTAL_STATE
from vertnet.parsers.sex import SEX
from vertnet.parsers.tail_length import TAIL_LENGTH
from vertnet.parsers.testes_size import TESTES_SIZE
from vertnet.parsers.testes_state import TESTES_STATE
from vertnet.parsers.total_length import TOTAL_LENGTH
from vertnet.parsers.tragus_length import TRAGUS_LENGTH
from vertnet.parsers.vagina_state import VAGINA_STATE

TRAITS = {
    'body_mass': BODY_MASS,
    'ear_length': EAR_LENGTH,
    'embryo_count': EMBRYO_COUNT,
    'embryo_length': EMBRYO_LENGTH,
    'forearm_length': FOREARM_LENGTH,
    'hind_foot_length': HIND_FOOT_LENGTH,
    'lactation_state': LACTATION_STATE,
    'life_stage': LIFE_STAGE,
    'nipple_count': NIPPLE_COUNT,
    'nipple_state': NIPPLE_STATE,
    'ovaries_size': OVARY_SIZE,
    'ovaries_state': OVARIES_STATE,
    'placental_scar_count': PLACENTAL_SCAR_COUNT,
    'placental_scar_state': PLACENTAL_SCAR_STATE,
    'pregnancy_state': PREGNANCY_STATE,
    'scrotal_state': SCROTAL_STATE,
    'sex': SEX,
    'tail_length': TAIL_LENGTH,
    'testes_size': TESTES_SIZE,
    'testes_state': TESTES_STATE,
    'total_length': TOTAL_LENGTH,
    'tragus_length': TRAGUS_LENGTH,
    'vagina_state': VAGINA_STATE,
    }
