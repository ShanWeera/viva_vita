from typing import List

from .constants import PredictionMethods, MhcISupertypes
from .wrappers import MhcINetMhcPan


class MhcIPredictionFactory(object):
    def __new__(
        cls,
        *,
        supertypes: List[MhcISupertypes],
        method: PredictionMethods = PredictionMethods.NETMHCPAN,
        length: int = 9,
        cutoff: float = 1.00,
    ):
        """
        This factory method should be use to get the appropriate prediction method.

        :param supertypes: A list of pre-defined MHC I supertypes.
        :param method: One of the pre-defined MHC I prediction methods (default: NETMHCPAN).
        :param length: The length of the generated epitopes (default: 9).
        :param cutoff: The IEDB percentile cutoff (default: 1%).

        :type supertypes: List[MhcISupertypes]
        :type method: PredictionMethods
        :type length: int
        :type cutoff: float

        Example:
            >>> from viva_vdm.core.iedb.mhci.constants import MhcISupertypes, PredictionMethods
            >>> from viva_vdm.core.iedb.mhci.factory import MhcIPredictionFactory
            >>> prediction_supertypes = [MhcISupertypes.A1, MhcISupertypes.A2]
            >>> predictor = MhcIPredictionFactory(supertypes=prediction_supertypes, method=PredictionMethods.NETMHCPAN)
            >>> results = predictor.predict("MDSNTVSSFQDI")
        """

        kwargs = locals()
        del kwargs['cls']

        if method == PredictionMethods.NETMHCPAN:
            return MhcINetMhcPan(**kwargs)
