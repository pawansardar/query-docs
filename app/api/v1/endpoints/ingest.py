from fastapi import APIRouter, Depends, File, UploadFile
from app.api.deps import get_document_vector_store, get_embedder
from app.db.vector.document_store import DocumentVectorStore
from app.services.ingestor import Ingestor
from app.services.embedder import GeminiEmbedder
from app.core.logging import get_logger

router = APIRouter()

logger =get_logger(__name__)

@router.post("/")
async def ingest(
    file: UploadFile = File(...),
    store: DocumentVectorStore = Depends(get_document_vector_store),
    embedder: GeminiEmbedder = Depends(get_embedder)
):
    logger.info("Ingest request received", extra={"file_name": file.filename})

    ingestor = Ingestor(store, embedder)
    await ingestor.ingest_file(file)

    logger.info("Ingestion completed", extra={"file_name": file.filename})

    return {"status": "success"}
