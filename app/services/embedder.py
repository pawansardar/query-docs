from google import genai

class GeminiEmbedder:
    def __init__(self):
        self.client = genai.Client()
        self.model = "gemini-embedding-001"
    
    def embed(self, text: list[str]):
        print(f"[DEBUG] Embedding {len(text)} texts")
        result = self.client.models.embed_content(
            model=self.model,
            contents=text
        )

        embeddings = [e.values for e in result.embeddings]

        return embeddings
