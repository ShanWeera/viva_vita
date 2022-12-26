import random
import string
import tempfile
import re

from subprocess import CompletedProcess, run, PIPE
from typing import Optional, List
from urllib.error import URLError, HTTPError

import backoff

from Bio import ExPASy
from Bio.ExPASy import Prosite
from Bio.ExPASy.Prosite import Record

from .exceptions import PrositeError
from .models import PrositeResult
from ..settings import AppConfig


class PrositeScan(object):
    ARG_MAP = {
        'report_optimum_alignment': '-a',
        'search_comp_strand': '-b',
        'is_fasta': '-f',
        'highest_cutoff_level_int': '-l',
        'highest_cutoff_leve_str': '-L',
        'individual_matches_circular': '-m',
        'use_raw_score': '-r',
        'prof_disjoint_unique': '-u',
        'cutoff_value': '-C',
        'normalization_mode': '-M',
        'length_limit': '-d',
        'output_xpsa': '-k',
        'list_seqs': '-s',
        'suppress_stderr_warnings': '-v',
        'output_psa': '-x',
        'alignment_human_readable': '-y',
        'show_prof_start_end': '-z',
        'output_width': '-W',
    }

    ENTRY_ID_PATTERN = re.compile(r'(?=PS)([^|]*)')
    START_END_PATTERN = re.compile(r'/(\d*)-(\d*)')

    def __init__(
        self,
        *,
        report_optimum_alignment: Optional[bool] = None,
        search_comp_strand: Optional[bool] = None,
        is_fasta: Optional[bool] = None,
        highest_cutoff_level_int: Optional[int] = None,
        highest_cutoff_leve_str: Optional[str] = None,
        individual_matches_circular: Optional[bool] = None,
        use_raw_score: Optional[bool] = None,
        prof_disjoint_unique: Optional[bool] = None,
        cutoff_value: Optional[int] = None,
        normalization_mode: Optional[int] = None,
        length_limit: Optional[bool] = None,
        output_xpsa: Optional[bool] = None,
        list_seqs: Optional[bool] = None,
        suppress_stderr_warnings: Optional[bool] = None,
        output_psa: Optional[bool] = None,
        alignment_human_readable: Optional[bool] = None,
        show_prof_start_end: Optional[bool] = None,
        output_width: Optional[int] = None,
    ):
        """
        This is the CLI API wrapper for the Prosite CLI tool.

        :param report_optimum_alignment: Report optimal alignment for all profiles.
        :param search_comp_strand: Search complementary strand of DNA sequences.
        :param is_fasta: Input sequence file is in FASTA format.
        :param highest_cutoff_level_int: Indicate highest cut-off level (number).
        :param highest_cutoff_leve_str: Indicate highest cut-off level (text).
        :param individual_matches_circular: Report individual matches for circular profiles.
        :param use_raw_score: Use raw score.
        :param prof_disjoint_unique: Force profile disjointness to UNIQUE.
        :param cutoff_value: Cut-off level to be used for match selection.
        :param normalization_mode: Set the normalization mode to use for the score computation.
        :param length_limit: Impose length limit on profile description.
        :param output_xpsa: Output using the xPSA header (using keyword=value pairs).
        :param list_seqs: List sequences of the matched regions.
        :param suppress_stderr_warnings: Suppress warnings on stderr.
        :param output_psa: List alignments in PSA format.
        :param alignment_human_readable: List alignments in human readable form.
        :param show_prof_start_end: Indicate profile start and stop positions.
        :param output_width: Specifies the output width.

        :type report_optimum_alignment: bool
        :type search_comp_strand: bool
        :type is_fasta: bool
        :type highest_cutoff_level_int: int
        :type highest_cutoff_leve_str: str
        :type individual_matches_circular: bool
        :type use_raw_score: bool
        :type prof_disjoint_unique: bool
        :type cutoff_value: int
        :type normalization_mode: int
        :type length_limit: int
        :type output_xpsa: bool
        :type list_seqs: bool
        :type suppress_stderr_warnings: bool
        :type output_psa: bool
        :type alignment_human_readable: bool
        :type show_prof_start_end: bool
        :type output_width: int

        Example:
            >>> from viva_vdm.core.prosite import PrositeScan
            >>> scanner = PrositeScan(output_xpsa=True, cutoff_value=-1, is_fasta=True, show_prof_start_end=True)
            >>> results = scanner.scan("SSVSSFERFEIFPKESSWPNHNTNGVTAACSHEGKSSFYRNLLWLTEKE")
        """

        self.report_optimum_alignment = report_optimum_alignment
        self.search_comp_strand = search_comp_strand
        self.is_fasta = is_fasta
        self.highest_cutoff_level_int = highest_cutoff_level_int
        self.highest_cutoff_leve_str = highest_cutoff_leve_str
        self.individual_matches_circular = individual_matches_circular
        self.use_raw_score = use_raw_score
        self.prof_disjoint_unique = prof_disjoint_unique
        self.cutoff_value = cutoff_value
        self.normalization_mode = normalization_mode
        self.length_limit = length_limit
        self.output_xpsa = output_xpsa
        self.list_seqs = list_seqs
        self.suppress_stderr_warnings = suppress_stderr_warnings
        self.output_psa = output_psa
        self.alignment_human_readable = alignment_human_readable
        self.show_prof_start_end = show_prof_start_end
        self.output_width = output_width

    def _generate_arguments(self) -> List[str]:
        """
        A central place to generate the arguments to be passed to Python subprocess.
        """

        arguments = list()

        for key, value in self.__dict__.items():
            if value is not None:
                flag = self.ARG_MAP.get(key)

                if not isinstance(value, bool):
                    arguments = [flag, str(value)] + arguments if flag else [str(value)] + arguments
                    continue

                arguments = [flag] + arguments

        settings = AppConfig()

        arguments = [settings.prosite_exe_path] + arguments
        arguments.append(settings.prosite_db_path)

        return arguments

    @classmethod
    def _run_prosite(cls, arguments: List[str]) -> CompletedProcess:
        """
        Runs the Prosite CLI tool.

        :param arguments: A list of arguments to pass to Python subprocess including the path to the Prosite binary.
        :type arguments: List[str]

        :return: A completed process that can then be used to get the stderr, stdout, etc.
        """

        return run(arguments, stderr=PIPE, stdout=PIPE)

    @classmethod
    @backoff.on_exception(backoff.expo, (URLError, HTTPError), max_time=600)
    def _get_prosite_entry(cls, accession: str) -> Record:
        """
        Uses the BioPython ExPASy wrapper to get more details about a Prosite entry using the public API.

        :param accession: A Prosite accession ID.
        :type accession: str

        :return: A Prosite record containing all details about the entry.
        """

        handle = ExPASy.get_prosite_raw(accession)
        record = Prosite.read(handle)
        handle.close()

        return record

    def _save_sequences_to_tempfile(self, sequence: str) -> str:
        """
        Converts the provided sequence into a FASTA file, and saves it in the temporary directory.

        :param sequence: An amino-acid sequence.
        :type sequence: str

        :return: An absolute path to a fle containing the FASTA sequence.
        """

        fasta_sequences = self._fasta_from_sequence(sequence)

        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write(fasta_sequences)

        return f.name

    @classmethod
    def _fasta_from_sequence(cls, sequence: str) -> str:
        """
        Converts a given sequence into FASTA format by randomly generating a FASTA header.

        :param sequence: An amino-acid sequence.
        :type sequence: str

        :return: A FASTA-formatted sequence.
        """

        random_string_list = [random.choice(string.ascii_uppercase) for _ in range(5)]

        return f'>{"".join(random_string_list)}\n{sequence}\n'

    @classmethod
    def _add_sequences_arg(cls, arguments: List[str], sequences_path: str) -> List[str]:
        """
        Adds the path to the temporary file we generated with the sequences to the list of arguments. It should be
        the second-last argument (as required by the Prosite tool) so we insert it at the appropriate index.

        :param arguments: The current list of arguments that does not include the sequence path.
        :param sequences_path: The path to the sequence file we generated.

        :type arguments: List[str]
        :type sequences_path: str

        :return: An updated list of arguments that contain the sequence path at the correct position.
        """

        length_of_current_args = len(arguments)
        arguments.insert((length_of_current_args - 1), sequences_path)

        return arguments

    def scan(self, sequence: str) -> List[PrositeResult]:
        """
        This is the main method of the Prosite class. First initialize the class with the desired configuration,
        and then use this method to run scan tool.

        :param sequence: An amino-acid sequence.
        :type sequence: str

        :return: A list of Prosite hits.
        """

        arguments = self._generate_arguments()
        sequences_file = self._save_sequences_to_tempfile(sequence)

        arguments = self._add_sequences_arg(arguments, sequences_file)
        process = self._run_prosite(arguments)

        if process.returncode != 0:
            raise PrositeError(process.stderr.decode('utf-8'))

        prosite_entries = list()
        results = process.stdout.decode('utf-8')

        entries = results.split(">")

        # The first element is empty so we remove it.
        entries.pop(0)

        for entry in entries:
            accession = re.search(self.ENTRY_ID_PATTERN, entry).group(0)
            start = re.search(self.START_END_PATTERN, entry).group(1)
            end = re.search(self.START_END_PATTERN, entry).group(2)

            remote_prosite_entry = self._get_prosite_entry(accession).__dict__

            remote_prosite_entry['start'] = start
            remote_prosite_entry['end'] = end

            prosite_entries.append(PrositeResult(**remote_prosite_entry))

        return prosite_entries
