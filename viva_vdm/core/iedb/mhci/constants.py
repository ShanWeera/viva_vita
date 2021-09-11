from enum import Enum
from pathlib import Path
from os.path import join
from typing import List, Literal

SUPERTYPES_DATA_DIR = join(Path(__file__).parent, "supertypes")

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


def get_alleles(
    supertype: Literal["A1", "A2", "A3", "A24", "A26", "B7", "B8", "B27", "B39", "B44", "B58", "B62"]
) -> List[str]:
    """
    Given a supertype name, reads the supertypes file in the supertypes directory, and returns a list of alleles.

    :param supertype: A pre-defined supertype name.
    :type supertype: Literal["A1", "A2", "A3", "A24", "A26", "B7", "B8", "B27", "B39", "B44", "B58", "B62"]

    :return: A list of alleles.
    """

    alleles = open(SUPERTYPE_ALLELE_MAP.get(supertype), 'r').readlines()

    return [allele.rstrip() for allele in alleles]


class MhcISupertypes(Enum):
    A1 = get_alleles('A1')
    A2 = get_alleles('A2')
    A3 = get_alleles("A3")
    A24 = get_alleles("A24")
    A26 = get_alleles("A26")
    B7 = get_alleles("B7")
    B8 = get_alleles("B8")
    B27 = get_alleles("B27")
    B39 = get_alleles("B39")
    B44 = get_alleles("B44")
    B58 = get_alleles("B58")
    B62 = get_alleles("B62")


class PredictionMethods(Enum):
    # TODO: Only NETMHCPAN is in the top 3 of benchmarks. Others either are not in the top 3, or do not produce results.
    #   Later implement mhcflurry and give users the option to choose the prediction method
    #   Also, some of these other methods do not support all the alleles in the supertypes we have defined
    #  (especially ANN, SMM)
    #   NETMHCPAN, PICKPOCKET, NETMHCPAN_EL support everything.
    NETMHCPAN_EL = "netmhcpan_el"
    # ANN = "ann"
    NETMHCPAN = "netmhcpan"
    PICKPOCKET = "pickpocket"
    # SMM = "smm"
    # SMMPMBEC = "smmpmbec"
    # CONSENSUS = "consensus"
    # NETMHCCONS = "netmhccons"
    # NETMHCSTABPAN = "netmhcstabpan"
    MHCFLURRY = 'mhcflurry'
