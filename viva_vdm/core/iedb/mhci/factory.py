from .constants import PredictionMethods, MhcISupertypes
from .wrappers import MhcINetMhcPan, MhcINetMhcPanEL, MhcIPickpocket, MhcFlurry


class MhcIPredictionFactory(object):
    def __new__(
        cls,
        *,
        supertype: MhcISupertypes,
        method: PredictionMethods = PredictionMethods.NETMHCPAN,
        length: int = 9,
        cutoff: float = 1.00,
    ):
        """
        This factory method should be use to get the appropriate prediction method.

        :param supertype: A pre-defined MHC I supertypes.
        :param method: One of the pre-defined MHC I prediction methods (default: NETMHCPAN).
        :param length: The length of the generated epitopes (default: 9).
        :param cutoff: The IEDB percentile cutoff (default: 1%).

        :type supertype: MhcISupertypes
        :type method: PredictionMethods
        :type length: int
        :type cutoff: float

        Example:
            >>> from viva_vdm.core.iedb.mhci.constants import MhcISupertypes, PredictionMethods
            >>> from viva_vdm.core.iedb.mhci.factory import MhcIPredictionFactory
            >>> prediction_supertype = MhcISupertypes.A1
            >>> predictor = MhcIPredictionFactory(supertypes=prediction_supertype, method=PredictionMethods.NETMHCPAN)
            >>> results = predictor.predict("MDSNTVSSFQDI")
        """

        kwargs = locals()
        del kwargs['cls']

        if method == PredictionMethods.NETMHCPAN:
            return MhcINetMhcPan(**kwargs)
        elif method == PredictionMethods.NETMHCPAN_EL:
            return MhcINetMhcPanEL(**kwargs)
        elif method == PredictionMethods.PICKPOCKET:
            return MhcIPickpocket(**kwargs)
        elif method == PredictionMethods.MHCFLURRY:
            return MhcFlurry(**kwargs)
