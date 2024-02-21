from fastapi import HTTPException


class HTTPUnauthorized(HTTPException):
    def __init__(self, **kwargs):
        kwargs.setdefault("detail", "Not authenticated")
        super(HTTPUnauthorized, self).__init__(401, **kwargs)


class HTTPForbidden(HTTPException):
    def __init__(self, **kwargs):
        kwargs.setdefault("detail", "Forbidden")
        super(HTTPForbidden, self).__init__(403, **kwargs)
