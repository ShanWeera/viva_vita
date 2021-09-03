from enum import Enum


class Databases(Enum):
    NON_REDUNDANT = 'nr'
    PDB = 'pdb'


class Matrices(Enum):
    BLOSSUM62 = 'BLOSUM62'
    PAM30 = 'PAM30'


class OutputFormats(Enum):
    JSON = 15
    XML = 16
