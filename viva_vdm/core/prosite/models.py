from typing import List

from pydantic import BaseModel


class PrositeResult(BaseModel):
    name: str
    type: str
    accession: str
    created: str
    data_update: str
    info_update: str
    pdoc: str
    description: str
    pattern: str
    matrix: List[str]
    rules: List
    prorules: List[str]
    postprocessing: List
    nr_sp_release: str
    nr_sp_seqs: int
    nr_total: List[int]
    nr_positive: List[int]
    nr_unknown: List[int]
    nr_false_pos: List[int]
    nr_false_neg: int
    nr_partial: int
    cc_taxo_range: str
    cc_max_repeat: str
    cc_site: List
    cc_skip_flag: str
    dr_positive: List[List[str]]
    dr_false_neg: List
    dr_false_pos: List
    dr_potential: List
    dr_unknown: List
    pdb_structs: List[str]
    cc_matrix_type: str
    cc_scaling_db: str
    cc_author: str
    cc_ft_key: str
    cc_ft_desc: str
    cc_version: str
    start: str
    end: str
