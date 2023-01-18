from pydantic import BaseModel


class PredictedEpitope(BaseModel):
    allele: str
    sequence: str
    percentile: float
