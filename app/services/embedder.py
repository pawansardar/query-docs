from google import genai
from app.core.logging import get_logger

class GeminiEmbedder:
    def __init__(self):
        self.client = genai.Client()
        self.model = "gemini-embedding-001"
        self.logger = get_logger(__name__)
    
    def embed(self, text: list[str]):
        if not text:
            return []
        
        self.logger.debug("Calling embedding model", extra={"batch_size": len(text)})

        try:
            result = self.client.models.embed_content(
                model=self.model,
                contents=text
            )
        except Exception as e:
            self.logger.exception("Embedding API call failed", extra={"batch_size": len(text), "model": self.model})
            raise

        if not result.embeddings:
            raise RuntimeError("Embedding API returned empty response")

        embeddings = [e.values for e in result.embeddings]

        return embeddings
