from pydantic import BaseModel


class PredictedEpitope(BaseModel):
    sequence: str
    percentile: float
