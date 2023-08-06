"""Collection of custom exception classes."""


class EmptyTransactionFile(RuntimeError):
    """Raised when a transaction file is read that doesn't contain any transactions."""

    def __init__(self, filepath, *args, **kwargs):
        self.filepath = filepath
        super().__init__(*args, **kwargs)
