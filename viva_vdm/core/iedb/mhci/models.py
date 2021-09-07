from pydantic import BaseModel


class MHCIResult(BaseModel):
    sequence: str
    percentile: float
