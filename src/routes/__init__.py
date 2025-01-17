from fastapi import APIRouter

router = APIRouter()


from .accounting import router as accounting_router

router.include_router(accounting_router)
