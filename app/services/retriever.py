from app.db.vector.document_store import DocumentVectorStore
from app.core.logging import get_logger
import asyncio
import time

class Retriever:
    def __init__(self, store: DocumentVectorStore, embedder):
        self.store = store
        self.embedder = embedder
        self.logger = get_logger(__name__)
    
    async def query(self, query: str):
        self.logger.info("Generating embeddings", extra={"query": query})

        start = time.time()
        embedding = await asyncio.to_thread(self.embedder.embed, [query])
        duration = time.time() - start

        self.logger.info("Embeddings created", extra={"query": query, "duration": round(duration, 3)})

        self.logger.info("Processing query", extra={"query": query})

        results = self.store.query(embedding=embedding[0])  # Use the first embedding because it's a single query

        texts = [
            {
                "text": point.payload.get("text"),
                "chunk_id": point.payload.get("chunk_id")
            }
            for point in results
        ]

        return texts
    