from .constants import PredictionMethods, MhcISupertypes
from viva_vdm.core.iedb.mhci import wrappers


class MhcIPredictionFactory(wrappers.MHCIPredictorBase):
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
            return wrappers.MhcINetMhcPan(**kwargs)
        elif method == PredictionMethods.NETMHCPAN_EL:
            return wrappers.MhcINetMhcPanEL(**kwargs)
        elif method == PredictionMethods.PICKPOCKET:
            return wrappers.MhcIPickpocket(**kwargs)
        elif method == PredictionMethods.SMM:
            return wrappers.MhcISMM(**kwargs)
        elif method == PredictionMethods.SMMPMBEC:
            return wrappers.MhcISMMPMBEC(**kwargs)
        elif method == PredictionMethods.CONSENSUS:
            return wrappers.MhcIConsensus(**kwargs)
        elif method == PredictionMethods.NETMHCCONS:
            return wrappers.MhcINetMhcCons(**kwargs)
        elif method == PredictionMethods.NETMHCSTABPAN:
            return wrappers.MhcINetMhcStabPan(**kwargs)
        elif method == PredictionMethods.ANN:
            return wrappers.MhcIANN(**kwargs)

        raise NotImplementedError(f'The method {method} is not implemented')
