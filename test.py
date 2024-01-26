from viva_vdm.core.iedb.mhcii.constants import MhcIISupertypes, PredictionMethods
from viva_vdm.core.iedb.mhcii.factory import MhcIIPredictionFactory

instance = MhcIIPredictionFactory(
    alleles=MhcIISupertypes.DP,
    method=PredictionMethods.CONSENSUS,
)

epitopes = instance.predict(
    ">YP_009047204.1 |Homo sapiens||2012\nMIHSVFLLMFLLTPTESYVDVGPDSVKSACIEVDIQQTFFDKTWPRPIDVSKADGIIYPQ"
)
print(instance.errors)
print(epitopes)
