from typing import List

from pydantic import BaseModel, Field


class SearchTarget(BaseModel):
    db: str


class Params(BaseModel):
    matrix: str
    expect: float
    gap_open: int
    gap_extend: int
    filter: str
    cbs: int


class DescriptionItem(BaseModel):
    id: str
    accession: str
    title: str
    taxid: int
    sciname: str


class Hsp(BaseModel):
    num: int
    bit_score: float
    score: int
    evalue: float
    identity: int
    positive: int
    query_from: int
    query_to: int
    hit_from: int
    hit_to: int
    align_len: int
    gaps: int
    qseq: str
    hseq: str
    midline: str


class Hit(BaseModel):
    num: int
    description: List[DescriptionItem]
    len: int
    hsps: List[Hsp]


class Stat(BaseModel):
    db_num: int
    db_len: int
    hsp_len: int
    eff_space: int
    kappa: float
    lambda_: float = Field(..., alias='lambda')
    entropy: float


class Search(BaseModel):
    query_id: str
    query_title: str
    query_len: int
    hits: List[Hit]
    stat: Stat


class Results(BaseModel):
    search: Search


class Report(BaseModel):
    program: str
    version: str
    reference: str
    search_target: SearchTarget
    params: Params
    results: Results


class BlastOutput2Item(BaseModel):
    report: Report


class BlastResults(BaseModel):
    BlastOutput2: List[BlastOutput2Item]
