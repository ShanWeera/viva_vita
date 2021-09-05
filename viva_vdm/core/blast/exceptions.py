from .constants import OutputFormats


class BlastException(Exception):
    def __init__(self, sequence: str, arguments: list, stderr: str):
        msg = f"Blast failed for sequence {sequence} with arguments {', '.join(arguments)}.\nThe error was: \n{stderr}"

        super(BlastException, self).__init__(msg)


class NotImplementedException(Exception):
    def __init__(self, method: OutputFormats):
        super(NotImplementedException, self).__init__(f"This output method is not implemented: {method}")
