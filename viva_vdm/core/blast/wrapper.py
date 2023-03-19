import asyncio
import json
import time
from typing import List, Optional, Literal

import requests

from .exceptions import BlastException
from ..settings import AppConfig
from .models import BlastResults

app_config = AppConfig()
BVU_BLAST_BASE_URL = 'https://blast.bezmialem.edu.tr'


class BlastCliWrapper(object):
    bvu_blast_url = f'{BVU_BLAST_BASE_URL}/job/create'
    bvu_blast_status_url = f'{BVU_BLAST_BASE_URL}/job/status/'
    bvu_blast_results_url = f'{BVU_BLAST_BASE_URL}/static/'

    def __init__(self, *, hcs: str, database: Literal['VNR', 'HumanNR', 'pdbaa'], exclude_taxid: Optional[int] = None):
        self.hcs = hcs
        self.exclude_taxid = exclude_taxid
        self.database = database

        self.job_ids = list()

    def _make_blast_post_request(self, hcs: str) -> str:
        data = dict(sequence=hcs, db=self.database)

        if self.exclude_taxid:
            data['exclude_taxid'] = self.exclude_taxid

        req = requests.post(
            url=self.bvu_blast_url,
            json=data,
            verify=False
        )

        req.raise_for_status()

        return req.content.decode('utf-8').strip('"')

    def _get_blast_results(self, job_id: str) -> BlastResults:
        complete = False

        while not complete:
            req = requests.get(url=f'{self.bvu_blast_status_url}{job_id}', verify=False)
            req.raise_for_status()

            status = req.content.decode('utf-8')
            status = int(status)

            if status == 3:
                complete = True
            elif status == 2:
                raise BlastException(job_id)
            else:
                time.sleep(10)
                continue

        results_request = requests.get(
            url=f'{self.bvu_blast_results_url}{job_id}.json',
            verify=False
        )

        results_request.raise_for_status()
        results_string = results_request.content.decode('utf-8')

        return BlastResults(**json.loads(results_string))

    def run_blast(self):
        job_id = self._make_blast_post_request(hcs=self.hcs)
        results = self._get_blast_results(job_id)

        return results
