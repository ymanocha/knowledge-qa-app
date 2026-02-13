from fastapi import APIRouter, UploadFile, File, HTTPException, Header, Depends
from typing import List, Optional
import time

from app.models import (
    Document, QueryRequest, QueryResponse, Citation, HealthResponse
)
from app.services.storage import vector_store
from app.services.llm import get_embedding, generate_answer, check_connection
from app.utils import clean_text, chunk_text

router = APIRouter()

async def get_session_id(x_session_id: Optional[str] = Header(None)):
    if not x_session_id:
        raise HTTPException(status_code=400, detail="X-Session-ID header is required")
    return x_session_id

@router.post("/upload", response_model=Document)
async def upload_file(
    file: UploadFile = File(...), 
    session_id: str = Depends(get_session_id)
):
    # 1. Validation
    if not file.filename.endswith(".txt"):
        raise HTTPException(status_code=400, detail="Only .txt files are allowed")
    
    # Read content
    content_bytes = await file.read()
    
    # Check size (10MB limit)
    if len(content_bytes) > 10 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File too large (Max 10MB)")
        
    try:
        text = content_bytes.decode("utf-8")
    except UnicodeDecodeError:
        raise HTTPException(status_code=400, detail="File must be valid UTF-8 text")
        
    # Check null bytes
    if '\0' in text:
        raise HTTPException(status_code=400, detail="File contains null bytes (binary file?)")
        
    # 2. Processing
    clean_txt = clean_text(text)
    if not clean_txt:
        raise HTTPException(status_code=400, detail="File is empty")
        
    chunks = chunk_text(clean_txt)
    
    # 3. Embedding & Storing
    doc_id = str(int(time.time())) # Simple ID
    
    for i, chunk in enumerate(chunks):
        # Embed
        vector = get_embedding(chunk)
        
        # Store with session_id
        vector_store.add(
            text=chunk,
            vector=vector,
            source=file.filename,
            session_id=session_id
        )
        
    return Document(
        id=doc_id,
        filename=file.filename,
        upload_date=time.strftime("%Y-%m-%d %H:%M:%S"),
        chunk_count=len(chunks)
    )

@router.post("/query", response_model=QueryResponse)
async def query_documents(
    request: QueryRequest, 
    session_id: str = Depends(get_session_id)
):
    # 1. Embed Query
    query_vec = get_embedding(request.question)
    
    # 2. Search (Isolated by session_id)
    results = vector_store.search(query_vec, session_id=session_id, k=request.k)
    
    # 3. Generate Answer
    if not results:
        return QueryResponse(answer="No relevant documents found in your session.", citations=[])
        
    context_chunks = [res["doc"]["text"] for res in results]
    
    try:
        answer = generate_answer(request.question, context_chunks)
    except Exception as e:
        answer = "I encountered an error generating the answer."
        print(f"LLM Error: {e}")

    # 4. Format Citations
    citations = []
    for res in results:
        doc = res["doc"]
        score = res["score"]
        citations.append(Citation(
            source_file=doc["source"],
            text_snippet=doc["text"][:200] + "...",
            chunk_id=doc["id"],
            score=score
        ))
        
    return QueryResponse(answer=answer, citations=citations)

@router.get("/documents", response_model=List[Document])
async def list_documents(session_id: str = Depends(get_session_id)):
    unique_docs = {}
    # Filter documents by session_id before aggregating
    user_docs = [doc for doc in vector_store.documents if doc.get("session_id") == session_id]
    
    for doc in user_docs:
        source = doc["source"]
        if source not in unique_docs:
            unique_docs[source] = {
                "id": source, 
                "filename": source,
                "upload_date": "Recent",
                "chunk_count": 0
            }
        unique_docs[source]["chunk_count"] += 1
        
    return list(unique_docs.values())

@router.delete("/documents/{file_id}")
async def delete_document(
    file_id: str, 
    session_id: str = Depends(get_session_id)
):
    # Pass session_id to ensure the user owns the document they are deleting
    success = vector_store.delete_document(file_id, session_id=session_id)
    if not success:
        raise HTTPException(status_code=404, detail="Document not found or access denied")
    return {"message": "Document deleted successfully"}

@router.get("/health", response_model=HealthResponse)
async def health_check():
    backend_status = "ok"
    storage_status = "ok" if vector_store else "error"
    llm_status = "ok" if check_connection() else "error"
    
    return HealthResponse(
        backend=backend_status,
        storage=storage_status,
        gemini=llm_status
    )
