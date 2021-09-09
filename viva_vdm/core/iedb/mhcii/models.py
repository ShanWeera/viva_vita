from ..common.models import PredictedEpitope


class MHCIIEpitope(PredictedEpitope):
    sequence: str
    percentile: float
