from typing import List

import requests
from fastapi import APIRouter, status, HTTPException
from fastapi_cache.decorator import cache

from viva_vdm.v1.endpoints.helpers.ncbi_taxonomy_response_helper import NCBITaxonomyResponseHelper
from viva_vdm.v1.models import TaxonomyDBSuggestion

router = APIRouter(prefix='/ncbi', tags=['ncbi'])


@router.get(
    '/taxdb/{query}',
    status_code=status.HTTP_200_OK,
    response_description="Returns a list of taxonomy IDs and their respective names",
    response_model=List[TaxonomyDBSuggestion],
)
@cache(expire=2.592e6)
async def get_suggested_taxonomy_ids(query: str) -> List[TaxonomyDBSuggestion]:
    """
    Get a list of HCS for the job ID

    If the provided job id is not found an HTTP 404 status is returned. A successful request will return an HTTP 200.
    """

    try:
        return NCBITaxonomyResponseHelper(query).get_taxonomy_suggestions()
    except requests.RequestException as ex:
        raise HTTPException(ex.request.status_code, f'Error querying NCBI Taxonomy database: {ex}')
