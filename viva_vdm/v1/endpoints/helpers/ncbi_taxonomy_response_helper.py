import re
from typing import List

import requests

from viva_vdm.v1.models import TaxonomyDBSuggestion


class NCBITaxonomyResponseHelper(object):
    REGEX_PATTERN_FOR_RESP = re.compile(r"new Array\((.*)\),")
    REGEX_PATTERN_FOR_TAXID = re.compile(r"(\d*$)")
    NCBI_TAXDB_ENDPOINT = 'https://blast.ncbi.nlm.nih.gov/portal/utils/autocomp.fcgi'

    def __init__(self, query: str):
        self.response = self._get_response(query)

    def _get_response(self, query: str) -> str:
        req = requests.get(self.NCBI_TAXDB_ENDPOINT, {'dict': 'blast_nr_prot_sg', 'q': query})

        req.raise_for_status()

        return req.text

    @classmethod
    def _sanitise_entry_data(cls, entry_data: str):
        entry_data = entry_data.replace('\n', '')

        return entry_data

    def get_taxonomy_suggestions(self) -> List[TaxonomyDBSuggestion]:
        matches = self.REGEX_PATTERN_FOR_RESP.findall(self.response)

        if not matches:
            return list()

        result_list = eval(f'[{matches[0]}]')

        taxonomy_suggestions = list()
        for item in result_list:
            sanitised_item = self._sanitise_entry_data(item)
            matches = self.REGEX_PATTERN_FOR_TAXID.findall(sanitised_item)

            if not matches:
                continue

            tax_id = matches[0]

            try:
                taxonomy_suggestions.append(TaxonomyDBSuggestion(label=sanitised_item, value=f'{tax_id}', taxid=tax_id))
            except Exception:
                print(tax_id)

        return taxonomy_suggestions
