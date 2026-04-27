from app.db.vector.document_store import DocumentVectorStore
from fastapi import UploadFile
from pypdf import PdfReader
import asyncio

class Ingestor:
    def __init__(self, store: DocumentVectorStore, embedder):
        self.store = store
        self.embedder = embedder
    
    async def ingest_file(self, file: UploadFile):
        file_name = file.filename
        print(f"[DEBUG] Ingesting file: {file_name}")

        if not file_name.lower().endswith((".pdf", ".txt")):
            raise ValueError(f"[ERROR] Unsupported file type: {file_name}. Only PDF and TXT files are supported.")

        if file_name.lower().endswith(".pdf"):
            text = await asyncio.to_thread(self.read_pdf, file)
        else:
            text = (await file.read()).decode("utf-8", errors="ignore")  # Decode TXT
        
        chunks = self.chunk_text(text)

        if not chunks:
            raise ValueError(f"[ERROR] No content to ingest in {file_name}")

        embeddings = await asyncio.to_thread(self.embedder.embed, chunks)

        self.store.add_documents(texts=chunks, embeddings=embeddings, file_name=file_name)
    
    def read_pdf(self, file: UploadFile):
        file.file.seek(0)
        reader = PdfReader(file.file)

        text = ""

        for page in reader.pages:
            text += page.extract_text() or ""

        print(f"[DEBUG] Read {len(text)} characters from {file.filename}")

        if not text.strip():
            raise ValueError(f"[ERROR] No text found in {file.filename}")
        
        return text
    
    def chunk_text(self, text, chunk_size=500, overlap=50):
        chunks = []
        start = 0

        if overlap >= chunk_size:
            raise ValueError("[ERROR] Overlap must be less than chunk size")
        
        while start < len(text):
            end = min(start + chunk_size, len(text))
            chunk = text[start:end]
            chunks.append(chunk)
            start += chunk_size - overlap

        print(f"[DEBUG] Created {len(chunks)} chunks from {len(text)} characters")

        return chunks
    