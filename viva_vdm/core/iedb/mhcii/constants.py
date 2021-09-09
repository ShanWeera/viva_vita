from enum import Enum
from pathlib import Path
from os.path import join
from typing import List, Literal

SUPERTYPES_DATA_DIR = join(Path(__file__).parent, "supertypes")

SUPERTYPE_ALLELE_MAP = {
    'DR': join(SUPERTYPES_DATA_DIR, "supertype_dr.txt"),
    'DP': join(SUPERTYPES_DATA_DIR, "supertype_dp.txt"),
    'DQ': join(SUPERTYPES_DATA_DIR, "supertype_dq.txt"),
}


def get_alleles(supertype: Literal["DR", "DP", "DQ"]) -> List[str]:
    """
    Given a supertype name, reads the supertypes file in the supertypes directory, and returns a list of alleles.

    :param supertype: A pre-defined supertype name.
    :type supertype: Literal["DR", "DP", "DQ"]

    :return: A list of alleles.
    """

    print(SUPERTYPE_ALLELE_MAP.get(supertype))
    alleles = open(SUPERTYPE_ALLELE_MAP.get(supertype), 'r').readlines()

    return [allele.rstrip() for allele in alleles]


class MhcIISupertypes(Enum):
    DR = get_alleles('DR')
    DP = get_alleles('DP')
    DQ = get_alleles("DQ")


class PredictionMethods(Enum):
    CONSENSUS = "consensus"
    NETMHCIIPAN = "NetMHCIIpan"
    NNALIGN = "nn_align-2.3"
    SMMALIGN = "smm_align"
    TEPITOPE = "tepitope"
    COMBLIB = "comblib"
    NETMHCPAN_EL = "netmhciipan_el"
    NETMHCPAN_BA = "netmhciipan_ba"
