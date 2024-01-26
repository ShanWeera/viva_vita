from pydantic import BaseModel


class PredictedEpitope(BaseModel):
    allele: str
    sequence: str
    percentile: float
    success: bool
    start: int
    end: int
