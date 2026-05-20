from fastapi import Request, Response
from starlette.responses import JSONResponse

from src.repositories.exceptions import RepositoryError, DuplicateError
from src.services.exceptions import BusinessError


def duplicate_error_handler(request: Request, exc: DuplicateError) -> Response:
    return JSONResponse(
        status_code=409,
        content={
            "success": False,
            "error": exc.message,
            "error_code": exc.error_code,
        },
    )


def repository_error_handler(request: Request, exc: RepositoryError) -> Response:
    return JSONResponse(
        status_code=400,
        content={
            "success": False,
            "error": exc.message,
            "error_code": exc.error_code,
        },
    )


def business_error_handler(request: Request, exc: BusinessError) -> Response:
    return JSONResponse(
        status_code=400,
        content={
            "success": False,
            "error": exc.message,
            "error_code": exc.error_code,
        },
    )
