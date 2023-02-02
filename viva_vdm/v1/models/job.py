from typing import List

from pydantic import BaseModel, Field

from viva_vdm.core.models import MHCIPredictionMethods, MHCIIPredictionMethods


class HCSApiModel(BaseModel):
    sequence: str = Field(..., title='The sequence of the HCS')
    incidence: float = Field(..., title='The incidence of the HCS in the MSA')
    position: int = Field(..., title='The position at which this HCS was observed in the MSA')


class JobHCSListModel(HCSApiModel):
    id: str = Field(..., title='Automatically generated ID for the HCS', alias='_id')


class CreateJobRequest(BaseModel):
    """
    This is the API model for a job submit request.
    """

    taxonomy_id: int = Field(..., title='Taxonomy ID of the virus')
    protein_name: str = Field('Unknown Protein', title='The name of the protein being analysed')
    hcs: List[HCSApiModel] = Field(..., title='The HCS to analyse')
    mhci_prediction_method: MHCIPredictionMethods = Field(
        MHCIPredictionMethods.NETMHCPAN, title='IEDB MHCI prediction method to use'
    )
    mhcii_prediction_method: MHCIIPredictionMethods = Field(
        MHCIIPredictionMethods.NETMHCIIPAN, title='IEDB MHCII prediction method to use'
    )
