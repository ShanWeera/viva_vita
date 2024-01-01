from abc import ABC, abstractmethod
from typing import List, TypeVar, TypedDict, ClassVar

from ttp import ttp

T = TypeVar('T')

ErrorType = TypedDict('ErrorType', {'allele': str, 'errors': str})


class PredictorBase(ABC):
    errors: ClassVar[List[ErrorType]] = []

    def __init__(
        self,
        *,
        alleles: List[str],
        method: str,
        length: int,
        cutoff: float,
    ):
        if not all((alleles, method, length, cutoff)):
            raise ValueError('Alleles, length, method and cutoff values need to be provided')

        self.alleles = alleles
        self.length = length
        self.method = method
        self.cutoff = cutoff

        self.errors = []

    @abstractmethod
    def get_table_template(self):
        raise NotImplementedError()

    @abstractmethod
    def run_prediction_process(self, allele: str, sequence: str) -> tuple[str, str]:
        raise NotImplementedError()

    def predict(self, sequence: str) -> List[dict]:
        results: List[dict] = list()

        for allele in self.alleles:
            output, errors = self.run_prediction_process(allele, sequence)

            if errors:
                self.errors.append({'allele': allele, 'errors': errors})
                continue

            _, rows = output.split('\n', 1)

            results_list = self.parse_results_table(rows)

            results.extend(results_list)

        return results

    def parse_results_table(self, results_table: str) -> List[dict]:
        template = self.get_table_template()
        parser = ttp(data=results_table, template=template)
        parser.parse()

        parsed_rows = parser.result(structure='flat_list')

        return parsed_rows
