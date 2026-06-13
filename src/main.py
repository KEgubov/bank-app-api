import uvicorn
from fastapi import FastAPI

from src.api import main_router
from src.api.exception_handlers import (
    duplicate_error_handler,
    repository_error_handler,
    business_error_handler,
)
from src.configs.auth_config import security
from src.repositories.exceptions import DuplicateError, RepositoryError
from src.services.exceptions import BusinessError

app = FastAPI(title="BankApp API")

app.include_router(main_router)

security.handle_errors(app)

app.add_exception_handler(DuplicateError, duplicate_error_handler)
app.add_exception_handler(RepositoryError, repository_error_handler)
app.add_exception_handler(BusinessError, business_error_handler)
