"""All of the parsers."""

from src.parsers.body_mass import BODY_MASS
from src.parsers.ear_length import EAR_LENGTH
from src.parsers.embryo_count import EMBRYO_COUNT
from src.parsers.embryo_length import EMBRYO_LENGTH
from src.parsers.forearm_length import FOREARM_LENGTH
from src.parsers.hind_foot_length import HIND_FOOT_LENGTH
from src.parsers.lactation_state import LACTATION_STATE
from src.parsers.life_stage import LIFE_STAGE
from src.parsers.nipple_count import NIPPLE_COUNT
from src.parsers.nipple_state import NIPPLE_STATE
from src.parsers.ovaries_size import OVARY_SIZE
from src.parsers.ovaries_state import OVARIES_STATE
from src.parsers.placental_scar_count import PLACENTAL_SCAR_COUNT
from src.parsers.pregnancy_state import PREGNANCY_STATE
from src.parsers.sex import SEX
from src.parsers.tail_length import TAIL_LENGTH
from src.parsers.testes_size import TESTES_SIZE
from src.parsers.testes_state import TESTES_STATE
from src.parsers.total_length import TOTAL_LENGTH
from src.parsers.tragus_length import TRAGUS_LENGTH

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
    'pregnancy_state': PREGNANCY_STATE,
    'sex': SEX,
    'tail_length': TAIL_LENGTH,
    'testes_size': TESTES_SIZE,
    'testes_state': TESTES_STATE,
    'total_length': TOTAL_LENGTH,
    'tragus_length': TRAGUS_LENGTH,
    }
