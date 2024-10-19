from fastapi import APIRouter

from .index import index_router
from .categories import categories_router
from .products import products_router

root_router = APIRouter()

root_router.include_router(
    categories_router,
    prefix="/categories",
    tags=["categories"]
)
root_router.include_router(
    products_router,
    prefix="/products",
    tags=["products"]

)
root_router.include_router(
    index_router,
)
