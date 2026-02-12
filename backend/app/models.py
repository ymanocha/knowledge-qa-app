from pydantic import BaseModel
from typing import List, Dict, Optional

class Document(BaseModel):
    id: str
    filename: str
    upload_date: str
    chunk_count: int

class Citation(BaseModel):
    source_file: str
    text_snippet: str
    chunk_id: int
    score: float

class QueryRequest(BaseModel):
    question: str
    k: int = 3

class QueryResponse(BaseModel):
    answer: str
    citations: List[Citation]

class HealthResponse(BaseModel):
    backend: str
    storage: str
    gemini: str
