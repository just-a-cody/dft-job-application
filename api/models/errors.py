"""Models for errors"""

from pydantic import BaseModel


class ErrorModel(BaseModel):
    """General error pydantic base model"""

    detail: str


class DatabaseOperationError(Exception):
    """Custom exception for database operations"""


class DatabaseNotFoundError(Exception):
    """Custom exception for database cannot find a record"""
