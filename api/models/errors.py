from pydantic import BaseModel

"""
Custom errors models
"""


class ErrorModel(BaseModel):
    detail: str


"""
Custom Error Exceptions
"""


class InternalServerException(Exception):
    pass


class NotFoundException(Exception):
    pass
