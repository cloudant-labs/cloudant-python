"""For when stuff breaks :D"""

HTTP_SUCCESS_RANGE = range(200, 300)


class DivanException(Exception):

    """Base class for all Divan exceptions."""

    def __init__(self, response):
        self.response = response

    def __str__(self):
        return repr(self.response.status_code)


class NotFoundError(DivanException, LookupError):
    pass


class UnauthorizedError(DivanException):
    pass


class ForbiddenError(DivanException):
    pass


class BadRequestError(DivanException, SyntaxError):
    pass


class MethodNotAllowedError(DivanException, AttributeError):
    pass


class ConflictError(DivanException, AssertionError):
    pass

ERROR_CODES = {
    400: BadRequestError,
    401: UnauthorizedError,
    402: ForbiddenError,
    404: NotFoundError,
    405: MethodNotAllowedError,
    409: ConflictError
}

def validate(response):
    if response.status_code not in HTTP_SUCCESS_RANGE:
        if response.status_code in ERROR_CODES.keys():
            raise ERROR_CODES[response.status_code](response)
        else:
            raise DivanException(response)