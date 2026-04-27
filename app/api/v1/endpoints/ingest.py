from fastapi import APIRouter, Depends, File, UploadFile
from app.api.deps import get_document_vector_store, get_embedder
from app.db.vector.document_store import DocumentVectorStore
from app.services.ingestor import Ingestor
from app.services.embedder import GeminiEmbedder

router = APIRouter()

@router.post("/")
async def ingest(
    file: UploadFile = File(...),
    store: DocumentVectorStore = Depends(get_document_vector_store),
    embedder: GeminiEmbedder = Depends(get_embedder)
):
    ingestor = Ingestor(store, embedder)
    await ingestor.ingest_file(file)
    return
