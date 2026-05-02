from qdrant_client.models import Distance, VectorParams, PointStruct, Filter, FieldCondition, MatchValue
import uuid
from app.core.logging import get_logger

class DocumentVectorStore:
    def __init__(self, client, vector_size: int = 3072):
        self.client = client
        self.collection_name = "documents"
        self.vector_size = vector_size
        self._ensure_collection()
        self.logger = get_logger(__name__)
    
    def _ensure_collection(self):
        if not self.client.collection_exists(self.collection_name):
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=self.vector_size,
                    distance=Distance.COSINE
                )
            )

    def add_documents(self, texts: list[str], embeddings: list[list[float]], file_name: str, user_id="user1"):
        points = []

        if len(texts) != len(embeddings):
            raise ValueError("Mismatch between texts and embeddings")

        try:
            for i, (text, vector) in enumerate(zip(texts, embeddings)):
                if len(vector) != self.vector_size:
                    raise ValueError(f"Expected vector of size {self.vector_size} but got {len(vector)}")
                
                points.append(
                    PointStruct(
                        id=str(uuid.uuid4()),
                        vector=vector,
                        payload={
                            "user_id": user_id,
                            "text": text,
                            "file_name": file_name,
                            "chunk_id": f"{file_name}_chunk_{i}"
                        }
                    )
                )
            
            self.logger.info("Adding documents to collection", extra={"file_name": file_name, "points_size": len(points), "collection_name": self.collection_name})

            batch_size = 100

            for i in range(0, len(points), batch_size):
                batch = points[i:i+batch_size]
                
                self.client.upsert(
                    collection_name=self.collection_name,
                    points=batch
                )
                
                self.logger.info("Added documents to database collection", extra={"file_name": file_name, "batch_size": len(batch), "collection_name": self.collection_name})
            
        except Exception as e:
            self.logger.exception("Failed to add documents to collection", extra={"file_name": file_name, "collection_name": self.collection_name})
            raise
    
    def get_all_points_debug(self):
        all_points = []
        offset = None
        
        while True:
            points, offset = self.client.scroll(
                collection_name=self.collection_name,
                limit=100,
                offset=offset
            )
            all_points.extend(points)

            if offset is None:
                break

        return all_points
    
    def query(self, embedding: list[float], user_id = "user1") -> list[PointStruct]:
        self.logger.info("Querying collection", extra={"collection_name": self.collection_name})
        try:
            search_result = self.client.query_points(
                collection_name=self.collection_name,
                query=embedding,
                query_filter=Filter(
                    must=[
                        FieldCondition(
                            key="user_id",
                            match=MatchValue(value=user_id)
                        )
                    ]
                ),
                with_payload=True,
                with_vectors=False,
                limit=10
            ).points

            self.logger.info(
                "Queried collection",
                extra={
                    "collection_name": self.collection_name,
                    "results": len(search_result),
                    "top_score": search_result[0].score if search_result else None
                }
            )

            self.logger.debug(
                "Queried collection",
                extra={
                    "collection_name": self.collection_name,
                    "results": [
                        {
                            "id": point.id,
                            "score": point.score,
                            "file_name": point.payload.get("file_name"),
                            "text_preview": (point.payload.get("text") or "")[:200]
                        }
                        for point in search_result[:5]
                    ]
                }
            )

            return search_result
        
        except Exception as e:
            self.logger.exception("Failed to query collection", extra={"collection_name": self.collection_name})
            raise
    