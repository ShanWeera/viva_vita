import json
from os import environ
from subprocess import run, PIPE
from typing import List

from .constants import Databases, OutputFormats, Matrices
from .exceptions import BlastException, NotImplementedException
from ..settings import AppConfig
from .models import BlastResults

app_config = AppConfig()


class BlastCliWrapper(object):
    def __init__(
        self,
        *,
        database: Databases = Databases.NON_REDUNDANT,
        matrix: Matrices = Matrices.PAM30,
        evalue: float = 0.05,
        outfmt: OutputFormats = OutputFormats.JSON,
        remote: bool = True,
        tax_ids_exclude: list = None,
        tax_ids_include: list = None,
        max_target_seqs: int = 10,
    ):

        """
        A wrapper for the BLAST+ cli tool.

        :param database: The code of the database to query against.
        :param matrix: The matrix to use.
        :param evalue: Expect value (E) for saving hits.
        :param outfmt: The output format of results.
        :param remote: To use local database, or public NCBI database.
        :param tax_ids_exclude: List of taxonomy ids to exclude in the search.
        :param tax_ids_include: List of taxonomy ids to include in the search.
        :param max_target_seqs: Number of aligned sequences to keep.

        :type database: Databases
        :type matrix: Matrices
        :type evalue: float
        :type outfmt: OutputFormats
        :type remote: bool
        :type tax_ids_exclude: list
        :type tax_ids_include: list
        :type max_target_seqs: int

        Example:
        >>> from viva_vdm.core.blast import BlastCliWrapper
        >>> results = BlastCliWrapper().run_blast('SSVSSFERFEIFPKESSWPNHNTNGVTAACSHEGKSSFYRNLLWLTEKE')
        """

        if tax_ids_exclude is None:
            tax_ids_exclude = []

        if tax_ids_include is None:
            tax_ids_include = []

        self.database = database
        self.matrix = matrix
        self.evalue = evalue
        self.outfmt = outfmt
        self.remote = remote
        self.tax_ids_exclude = tax_ids_exclude
        self.max_target_seqs = max_target_seqs
        self.tax_ids_include = tax_ids_include

    def run_blast(self, sequence: str) -> BlastResults:
        """
        Run BLAST with the provided parameters as class initiation.

        :param sequence: The sequence to perform BLAST with.
        :type sequence: str

        :return: Returns the BLAST results in the output format provided at initiation.
        """

        arguments = self._get_blast_args()

        # Without the system environment vars blast's connection to NCBI fails. Not really sure why but adding this
        # helps
        current_envars = environ.copy()

        process = run(
            arguments,
            stdout=PIPE,
            stderr=PIPE,
            encoding='ascii',
            input=sequence,
            env={**current_envars, 'BLASTDB': app_config.blastdb_path},
        )

        if process.returncode != 0:
            raise BlastException(sequence, arguments, process.stderr)

        if self.outfmt != OutputFormats.JSON:
            raise NotImplementedException(self.outfmt.name)

        return BlastResults(**json.loads(process.stdout))

    def _get_blast_args(self) -> list:
        """
        Get the arguments for subprocess based on the provided parameters.

        :return: A list of parameters.
        """

        settings = AppConfig()

        args = [
            settings.blast_exe_path,
            '-db',
            self.database.value,
            '-matrix',
            self.matrix.value,
            '-evalue',
            str(self.evalue),
            '-outfmt',
            str(self.outfmt.value),
            '-remote' if self.remote else None,
            '-max_target_seqs',
            str(self.max_target_seqs),
        ]

        filter_args = self._get_tax_filter_args()

        if filter_args:
            args = args + filter_args

        args = [arg for arg in args if arg]

        return args

    def _get_tax_filter_args(self) -> List[str]:
        """
        A common method to generate the taxonomy filtering parameters.

        :return: A list containing the appropriate taxonomy filtering parameters.
        """

        if self.tax_ids_include or self.tax_ids_exclude:
            if self.remote:
                return self._get_entrez_query()
            else:
                return self._get_taxid_arguments()

    def _get_taxid_arguments(self) -> List[str]:
        """
        Generates a list of arguments for including and excluding given taxonomy ids.

        :return: A list of arguments.
        """

        args = []

        if self.tax_ids_include:
            args.append('-taxids')
            args.append(','.join(str(tax_id) for tax_id in self.tax_ids_include))

        if self.tax_ids_exclude:
            args.append('-negative_taxids')
            args.append(','.join(str(tax_id) for tax_id in self.tax_ids_exclude))

        return args

    def _get_entrez_query(self) -> List[str]:
        """
        Generates entrez query with the given filtering criteria.

        :return: A list containing the flag and query string for entrez.
        """

        if self.remote:
            # In remote mode we cannot use *-taxids, we have to use entrez queries.
            entrez_query = str()
            args = ['-entrez_query']

            if self.tax_ids_include:
                for count, idx in enumerate(self.tax_ids_include, 1):
                    entrez_query += f'(txid{idx} [ORGN]){" AND " if count != len(self.tax_ids_include) else " "}'
            else:
                entrez_query += 'all [filter] '

            if self.tax_ids_exclude:
                for count, idx in enumerate(self.tax_ids_exclude, 1):
                    entrez_query += f'NOT (txid{idx} [ORGN]){" AND " if count != len(self.tax_ids_exclude) else ""}'

            args.append(f'{entrez_query}')

            return args
