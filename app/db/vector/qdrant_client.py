from qdrant_client import QdrantClient

def get_client():
    return QdrantClient(url="http://localhost:6333")
