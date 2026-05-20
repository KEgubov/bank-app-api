class RepositoryError(Exception):
    def __init__(self, message, error_code: str = "VALIDATION_ERROR"):
        self.message = message
        self.error_code = error_code
        super().__init__(message)