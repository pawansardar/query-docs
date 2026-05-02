from pydantic import BaseModel

class QueryRequest(BaseModel):
    query: str

class QueryResult(BaseModel):
    text: str
    chunk_id: str | None = None

class QueryResponse(BaseModel):
    results: list[QueryResult]
