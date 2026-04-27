from app.db.vector.qdrant_client import get_client
from app.services.embedder import GeminiEmbedder
from app.db.vector.document_store import DocumentVectorStore

def get_document_vector_store():
    client = get_client()
    return DocumentVectorStore(client)

def get_embedder():
    return GeminiEmbedder()
