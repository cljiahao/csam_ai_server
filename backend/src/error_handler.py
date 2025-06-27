from fastapi import FastAPI, HTTPException, Request

from core.exceptions import ImageProcessError, InvalidInputError, NoResultsFound


# TODO: pytest
def configure_exceptions(app: FastAPI):
    """
    Configures custom exception handlers for the FastAPI application.

    Args:
        app: The FastAPI application instance.
    """

    @app.exception_handler(InvalidInputError)
    async def handle_invalid_input_error(request: Request, exc: NoResultsFound):
        raise HTTPException(status_code=404, detail=str(exc))

    @app.exception_handler(ImageProcessError)
    async def handle_image_process_error(request: Request, exc: ImageProcessError):
        raise HTTPException(status_code=404, detail=str(exc))

    @app.exception_handler(NoResultsFound)
    async def handle_no_results_found_error(request: Request, exc: NoResultsFound):
        raise HTTPException(status_code=404, detail=str(exc))

    @app.exception_handler(ValueError)
    async def handle_value_error(request: Request, exc: NoResultsFound):
        raise HTTPException(status_code=404, detail=str(exc))
