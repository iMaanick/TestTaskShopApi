from fastapi import APIRouter

from .index import index_router
from .categories import categories_router

root_router = APIRouter()

root_router.include_router(
    categories_router,
    prefix="/categories",
)
root_router.include_router(
    index_router,
)
