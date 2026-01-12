class DetailedError(Exception):
    def __init__(self, error: str, detail: str | None = None):
        self.error = error
        self.detail = detail
