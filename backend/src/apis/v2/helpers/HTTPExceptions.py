from fastapi import HTTPException, status

from core.logging import logger
from core.exceptions import (
    DatabaseError,
    ImageProcessError,
    MissingSettings,
    InvalidInputError,
    NoResultsFound,
    CacheError,
)


def handle_exceptions(e: Exception) -> None:
    """Handles exceptions by raising HTTPExceptions."""

    if isinstance(
        e,
        (
            FileNotFoundError,
            MissingSettings,
            ValueError,
            InvalidInputError,
            NoResultsFound,
        ),
    ):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.args[0])
    elif isinstance(e, (DatabaseError, ImageProcessError, CacheError)):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=e.args[0]
        )
    else:
        logger.error(str(e), exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Bad Request: The request was invalid or cannot be served.",
        )
