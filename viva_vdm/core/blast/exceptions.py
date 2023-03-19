from .constants import OutputFormats


class BlastException(Exception):
    def __init__(self, job_id: str):
        msg = f'Error in Blast job {job_id}'

        super(BlastException, self).__init__(msg)


class NotImplementedException(Exception):
    def __init__(self, method: OutputFormats):
        super(NotImplementedException, self).__init__(f"This output method is not implemented: {method}")
