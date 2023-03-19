from fastapi import APIRouter, status, HTTPException
from mongoengine import DoesNotExist

from viva_vdm.core.models import HCSDBModel
from viva_vdm.v1.models.results import HCSResultsApiModel

router = APIRouter(prefix='/results', tags=['results'])


@router.get(
    '/hcs/{hcs_id}',
    status_code=status.HTTP_200_OK,
    response_description="Get all the results of a single HCS",
    response_model=HCSResultsApiModel,
)
def get_hcs_results(hcs_id: str) -> HCSResultsApiModel:
    """
    Get all the results of a single HCS.
    """

    try:
        hcs_instance = HCSDBModel.objects.get(id=hcs_id)
    except DoesNotExist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"HCS with id {hcs_id} does not exist")

    return HCSResultsApiModel(**hcs_instance.results.to_mongo().to_dict())
