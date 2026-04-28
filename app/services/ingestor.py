from app.db.vector.document_store import DocumentVectorStore
from fastapi import UploadFile
from pypdf import PdfReader
import asyncio
from app.core.logging import get_logger
import time

class Ingestor:
    def __init__(self, store: DocumentVectorStore, embedder):
        self.store = store
        self.embedder = embedder
        self.logger = get_logger(__name__)
    
    async def ingest_file(self, file: UploadFile):
        file_name = file.filename
        self.logger.info("Processing file", extra={"file_name": file_name})

        if not file_name.lower().endswith((".pdf", ".txt")):
            raise ValueError(f"Unsupported file type: {file_name}. Only PDF and TXT files are supported.")

        if file_name.lower().endswith(".pdf"):
            text = await asyncio.to_thread(self.read_pdf, file)
        else:
            text = (await file.read()).decode("utf-8", errors="ignore")  # Decode TXT
            self.logger.debug("Read TXT file", extra={"file_name": file_name})
        
        chunks = self.chunk_text(text)

        if not chunks:
            raise ValueError(f"No content to ingest in {file_name}")
        
        self.logger.info("Generating embeddings", extra={"file_name": file_name, "chunks": len(chunks)})
        
        start = time.time()
        embeddings = await asyncio.to_thread(self.embedder.embed, chunks)
        duration = time.time() - start

        self.logger.info("Embeddings created", extra={"file_name": file_name, "chunks": len(chunks), "duration": round(duration, 3)})

        self.store.add_documents(texts=chunks, embeddings=embeddings, file_name=file_name)
    
    def read_pdf(self, file: UploadFile):
        file.file.seek(0)
        reader = PdfReader(file.file)

        text = ""

        for page in reader.pages:
            text += page.extract_text() or ""

        self.logger.debug("Read PDF file", extra={"file_name": file.filename, "text_length": len(text)})

        if not text.strip():
            raise ValueError(f"No text found in {file.filename}")
        
        return text
    
    def chunk_text(self, text, chunk_size=500, overlap=50):
        chunks = []
        start = 0

        if overlap >= chunk_size:
            raise ValueError("Overlap must be less than chunk size")
        
        while start < len(text):
            end = min(start + chunk_size, len(text))
            chunk = text[start:end]
            chunks.append(chunk)
            start += chunk_size - overlap

        self.logger.debug("Created chunks from text", extra={"chunks": len(chunks), "chunk_size": chunk_size, "text_length": len(text)})

        return chunks
    