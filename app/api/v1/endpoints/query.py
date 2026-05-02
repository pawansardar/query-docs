from fastapi import APIRouter, Depends
from app.schemas.query import QueryRequest, QueryResponse
from app.api.deps import get_document_vector_store, get_embedder
from app.db.vector.document_store import DocumentVectorStore
from app.services.retriever import Retriever
from app.services.embedder import GeminiEmbedder
from app.core.logging import get_logger

router = APIRouter()

logger = get_logger(__name__)

@router.post("/")
async def query(
    request: QueryRequest,
    store: DocumentVectorStore = Depends(get_document_vector_store),
    embedder: GeminiEmbedder = Depends(get_embedder)
):
    query = request.query
    logger.info("Query request received", extra={"query": query})

    retriever = Retriever(store, embedder)
    results = await retriever.query(query=query)

    logger.info("Query completed", extra={"query": query, "results": len(results)})

    return QueryResponse(results=results)
