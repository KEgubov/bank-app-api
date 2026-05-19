from fastapi import APIRouter

from src.api.user_api import router as user_router
from src.api.account_api import router as account_router
from src.api.card_api import router as card_router
from src.api.contact_api import router as contact_router
from src.api.transaction_api import router as transaction_router
from src.api.auth_api import router as auth_router

main_router = APIRouter()

main_router.include_router(user_router)
main_router.include_router(account_router)
main_router.include_router(card_router)
main_router.include_router(contact_router)
main_router.include_router(transaction_router)
main_router.include_router(auth_router)