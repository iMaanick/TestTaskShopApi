from typing import Dict

from fastapi import APIRouter, Request

index_router = APIRouter()


@index_router.get("/")
def index(
        request: Request,
) -> Dict[str, str]:
    return {"Documentation": "http://127.0.0.1:8000/docs"}
