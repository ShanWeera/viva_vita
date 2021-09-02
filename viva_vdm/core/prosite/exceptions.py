class PrositeError(Exception):
    def __init__(self, error: str):
        super(PrositeError).__init__(f'Running Prosite CLI tool failed:\n\t{error}')
