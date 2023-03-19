from dataclasses import dataclass
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

    alleles = open(SUPERTYPE_ALLELE_MAP.get(supertype), 'r').readlines()

    return [allele.rstrip() for allele in alleles]


class MhcIISupertypes(Enum):
    DR = get_alleles('DR')
    DP = get_alleles('DP')
    DQ = get_alleles("DQ")


@dataclass
class PredictionMethods:
    # CONSENSUS = "consensus" doesn't work
    NETMHCIIPAN: str = "NetMHCIIpan"  # works for all alleles of all supertypes
    # NNALIGN: str = "nn_align-2.3" no results
    # SMMALIGN: str = "smm_align" doesn't work
    # TEPITOPE: str = "tepitope" doesn't support all the alleles in the supertypes
    # COMBLIB: str = "comblib" doesn't do all the alleles in the supertypes
    NETMHCPAN_EL: str = "netmhciipan_el"  # works for all alleles of all supertypes
    NETMHCPAN_BA: str = "netmhciipan_ba"  # works for all alleles of all supertypes
