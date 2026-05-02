from fastapi import APIRouter
from app.api.v1.endpoints.ingest import router as ingest_router
from app.api.v1.endpoints.debug import router as debug_router
from app.api.v1.endpoints.query import router as query_router

api_router = APIRouter()

api_router.include_router(ingest_router, prefix="/documents", tags=["documents"])
api_router.include_router(debug_router, prefix="/debug", tags=["debug"])
api_router.include_router(query_router, prefix="/queries", tags=["queries"])
