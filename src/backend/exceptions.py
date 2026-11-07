class AppExceptionError(Exception):
    """
    Root exception to all application exceptions
    """

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class NotFoundError(AppExceptionError):
    """
    Raised when a requested resource was not found
    """


class AlreadyExistsError(AppExceptionError):
    """
    Raised when a requested resource already exists
    """


class InvalidPasswordError(AppExceptionError):
    """
    Raised when a requested password is invalid
    """

    def __init__(self, message: str = "Password mismatch"):
        super().__init__(message)
