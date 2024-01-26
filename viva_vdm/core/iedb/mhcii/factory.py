from viva_vdm.core.iedb.mhcii.constants import PredictionMethods, MhcIISupertypes
from viva_vdm.core.iedb.mhcii import wrappers


class MhcIIPredictionFactory:
    def __new__(
        cls,
        *,
        alleles: MhcIISupertypes,
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
            return wrappers.MhcIINetMhcPan(**kwargs)

        if method == PredictionMethods.CONSENSUS:
            return wrappers.MhcIIConsensus(**kwargs)

        if method == PredictionMethods.NNALIGN:
            return wrappers.MhcIINnAlign(**kwargs)

        if method == PredictionMethods.SMMALIGN:
            return wrappers.MhcIISmmAlign(**kwargs)

        if method == PredictionMethods.COMBLIB:
            return wrappers.MhcIICombLib(**kwargs)

        if method == PredictionMethods.NETMHCPAN_EL:
            return wrappers.MhcIINetMhcPanEl(**kwargs)

        if method == PredictionMethods.NETMHCPAN_BA:
            return wrappers.MhcIINetMhcPanBa(**kwargs)

        raise NotImplementedError(f'The method {method} is not implemented')
