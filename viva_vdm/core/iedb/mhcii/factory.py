from viva_vdm.core.iedb.mhcii.constants import PredictionMethods, MhcIISupertypes
from viva_vdm.core.iedb.mhcii.wrappers import MhcIINetMhcPan


class MhcIIPredictionFactory(object):
    def __new__(
        cls,
        *,
        supertype: MhcIISupertypes,
        method: PredictionMethods = PredictionMethods.NETMHCIIPAN,
        length: int = 12,
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
            >>> predictor = MhcIIPredictionFactory(supertypes=prediction_supertype, method=PredictionMethods.NETMHCPAN)
            >>> results = predictor.predict("MDSNTVSSFQDI")
        """

        kwargs = locals()
        del kwargs['cls']

        if method == PredictionMethods.NETMHCIIPAN:
            return MhcIINetMhcPan(**kwargs)

        raise NotImplementedError(f'The method {method} is not implemented')
