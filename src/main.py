import uvicorn
from fastapi import FastAPI, Request, Response
from starlette.responses import JSONResponse

from src.api import main_router
from src.configs.auth_config import security
from src.services.exceptions import BusinessError

app = FastAPI()

app.include_router(main_router)

security.handle_errors(app)


@app.exception_handler(BusinessError)
def business_error_handler(request: Request, exc: BusinessError) -> Response:
    return JSONResponse(
        status_code=400,
        content={
            "success": False,
            "error": exc.message,
            "error_code": exc.error_code,
        },
    )


if __name__ == "__main__":
    uvicorn.run(app)
