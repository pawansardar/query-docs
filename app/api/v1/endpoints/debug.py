from fastapi import APIRouter, Depends
from app.api.deps import get_document_vector_store
from app.db.vector.document_store import DocumentVectorStore
from app.services.debugger import Debugger

router = APIRouter()

@router.get("/documents")
def debug(
    store: DocumentVectorStore = Depends(get_document_vector_store)
):
    debugger = Debugger(store)
    return debugger.get_collection_points()
