from typing import List

from pydantic import BaseModel, Field


class EpitopeApiModel(BaseModel):
    allele: str = Field(..., title='The allele that the epitope was predicted for')
    sequence: str = Field(..., title='The sequence of the epitope')
    percentile: float = Field(..., title='The percentile of the epitope')


class MHCIISupertypes(BaseModel):
    DR: List[EpitopeApiModel] = Field(None, title='MHCII Supertype DR')
    DP: List[EpitopeApiModel] = Field(None, title='MHCII Supertype DP')
    DQ: List[EpitopeApiModel] = Field(None, title='MHCII Supertype DQ')


class MHCISupertypes(BaseModel):
    A1: List[EpitopeApiModel] = Field(None, title='MHCI Supertype A1')
    A2: List[EpitopeApiModel] = Field(None, title='MHCI Supertype A2')
    A3: List[EpitopeApiModel] = Field(None, title='MHCI Supertype A3')
    A24: List[EpitopeApiModel] = Field(None, title='MHCI Supertype A24')
    A26: List[EpitopeApiModel] = Field(None, title='MHCI Supertype A26')
    B7: List[EpitopeApiModel] = Field(None, title='MHCI Supertype B7')
    B8: List[EpitopeApiModel] = Field(None, title='MHCI Supertype B8')
    B27: List[EpitopeApiModel] = Field(None, title='MHCI Supertype B27')
    B39: List[EpitopeApiModel] = Field(None, title='MHCI Supertype B39')
    B44: List[EpitopeApiModel] = Field(None, title='MHCI Supertype B44')
    B58: List[EpitopeApiModel] = Field(None, title='MHCI Supertype B58')
    B62: List[EpitopeApiModel] = Field(None, title='MHCI Supertype B62')


class PrositeApiModel(BaseModel):
    accession: str = Field(..., title='The accession number of the sequence')
    description: str = Field(..., title='The description of the sequence')
    start: int = Field(..., title='The start position of the sequence pattern')
    end: int = Field(..., title='The end position of the sequence pattern')


class BlastApiModel(BaseModel):
    accession: str = Field(..., title='The accession number')
    species: str = Field(..., title='The species to which this hit comes from')
    strain: str = Field(..., title='The strain')
    taxid: int = Field(..., title='The taxonomy ID')
    title: str = Field(..., title='The main title of the hit')


class HCSResultsApiModel(BaseModel):
    prosite: List[PrositeApiModel] = Field(None, title='Prosite results')
    blast: List[BlastApiModel] = Field(None, title='NCBI Blast results')
    mhci: MHCISupertypes = Field(None, title='IEDB MHCI prediction results')
    mhcii: MHCIISupertypes = Field(None, title='IEDB MHCII prediction results')
