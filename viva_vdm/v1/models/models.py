from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field

from ...core.models.models import MotifClasses


class Variant(BaseModel):
    sequence: str = Field(..., title='The amino-acid sequence of the variant.')
    count: int = Field(..., title='The number of times the variant was observed (frequency).')
    incidence: float = Field(..., title='The incidence of the variant.')
    motif_long: MotifClasses = Field(..., title='The class the variant belongs to.')
    metadata: dict = Field(..., title='Header metadata derived from the FASTA headers.')


class MotifIncidences(BaseModel):
    index: float = Field(..., title='The incidence of index at a kmer position.')
    major: float = Field(..., title='The incidence of major at a kmer position.')
    minor: float = Field(..., title='The incidence of minor at a kmer position.')
    unique: float = Field(..., title='The incidence of unique at a kmer position.')
    total: float = Field(..., title='The total variance at th e k-mer position (ie: excluding index)')
    distinct: float = Field(..., title='The incidence of distinct variants (ie: all except Index).')


class Position(BaseModel):
    position: int = Field(..., title='The kmer position.')
    support: int = Field(..., title='The number of supports that the kmer position has.')
    low_support: Optional[str] = Field(
        ..., title='If position has no (NS) or low support (LS), ' 'or support > threshold (null)'
    )
    variants: List[Variant] = Field(None, title='Kmer variants seen at the kmer position.')
    distinct_variants_count: int = Field(
        ..., title='The number of distinct variants at the k-mer position ' '(without index).'
    )
    incidences: MotifIncidences = Field(..., title='The incidence of the motif classes at a kmer position.')


class JobLogEntry(BaseModel):
    """
    The API model for a single log entry for a job.
    """

    id: str = Field(..., title='The id of the log entry.')
    flag: str = Field(..., title='The flag of the log entry indicating severity.')
    timestamp: datetime = Field(..., title='The time at which the log entry was produced.')
    message: str = Field(..., title='The message body of the log entry.')


class JobLogs(BaseModel):
    """
    The API model for a list of log entries of a job.
    """

    logs: List[JobLogEntry] = Field(..., title='List of log entries for the job.')
