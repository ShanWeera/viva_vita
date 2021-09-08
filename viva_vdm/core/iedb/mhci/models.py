from ..common.models import PredictedEpitope


class MHCIEpitope(PredictedEpitope):
    sequence: str
    percentile: float
