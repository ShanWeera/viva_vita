from enum import Enum
from pathlib import Path
from os.path import join
from typing import List

SUPERTYPES_DATA_DIR = join(Path(__file__).parent, "alleles")

SUPERTYPE_ALLELE_MAP = {
    'A1': join(SUPERTYPES_DATA_DIR, "supertype_a1.txt"),
    'A2': join(SUPERTYPES_DATA_DIR, "supertype_a2.txt"),
    'A3': join(SUPERTYPES_DATA_DIR, "supertype_a3.txt"),
    'A24': join(SUPERTYPES_DATA_DIR, "supertype_a24.txt"),
    'A26': join(SUPERTYPES_DATA_DIR, "supertype_a26.txt"),
    'B7': join(SUPERTYPES_DATA_DIR, "supertype_b7.txt"),
    'B8': join(SUPERTYPES_DATA_DIR, "supertype_b8.txt"),
    'B27': join(SUPERTYPES_DATA_DIR, "supertype_b27.txt"),
    'B39': join(SUPERTYPES_DATA_DIR, "supertype_b39.txt"),
    'B44': join(SUPERTYPES_DATA_DIR, "supertype_b44.txt"),
    'B58': join(SUPERTYPES_DATA_DIR, "supertype_b58.txt"),
    'B62': join(SUPERTYPES_DATA_DIR, "supertype_b62.txt"),
}


class MhcISupertypes(Enum):
    @classmethod
    def _get_alleles(cls, supertype: str) -> List[str]:
        alleles = open(SUPERTYPE_ALLELE_MAP.get(supertype), 'r').readlines()

        return [allele.rstrip() for allele in alleles]

    A1 = _get_alleles('A1')
    A2 = _get_alleles('A2')
    A3 = _get_alleles("A3")
    A24 = _get_alleles("A24")
    A26 = _get_alleles("A26")
    B7 = _get_alleles("B7")
    B8 = _get_alleles("B8")
    B27 = _get_alleles("B27")
    B39 = _get_alleles("B39")
    B44 = _get_alleles("B44")
    B58 = _get_alleles("B58")
    B62 = _get_alleles("B62")


class PredictionMethods(Enum):
    NETMHCPAN_EL = "netmhcpan_el"
    ANN = "ann"
    NETMHCPAN = "netmhcpan"
    PICKPOCKET = "pickpocket"
    SMM = "smm"
    SMMPMBEC = "smmpmbec"
