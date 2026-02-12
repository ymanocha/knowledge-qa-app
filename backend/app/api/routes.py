from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List
import time

from app.models import (
    Document, QueryRequest, QueryResponse, Citation, HealthResponse
)
from app.services.storage import vector_store
from app.services.llm import get_embedding, generate_answer, check_connection
from app.utils import clean_text, chunk_text

router = APIRouter()

@router.post("/upload", response_model=Document)
async def upload_file(file: UploadFile = File(...)):
    # 1. Validation
    if not file.filename.endswith(".txt"):
        raise HTTPException(status_code=400, detail="Only .txt files are allowed")
    
    if file.content_type != "text/plain":
         # Optional strict check, but filename check is often enough for this scope
         pass

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
    # We store chunks. The document ID will be the filename for simplicity in this MVP 
    # or we can generate a UUID.
    # But wait, Document model expects 'id'.
    # Let's use filename as a logical group, but store chunks individually.
    
    doc_id = str(int(time.time())) # Simple ID
    
    for i, chunk in enumerate(chunks):
        # Embed
        vector = get_embedding(chunk)
        
        # Store
        vector_store.add(
            text=chunk,
            vector=vector,
            metadata={
                "source": file.filename,
                "chunk_id": i,
                "doc_id": doc_id,
                "upload_timestamp": doc_id
            }
        )
        
    return Document(
        id=doc_id,
        filename=file.filename,
        upload_date=time.strftime("%Y-%m-%d %H:%M:%S"),
        chunk_count=len(chunks)
    )

@router.post("/query", response_model=QueryResponse)
async def query_documents(request: QueryRequest):
    # 1. Embed Query
    query_vec = get_embedding(request.question)
    
    # 2. Search
    results = vector_store.search(query_vec, k=request.k)
    
    # 3. Generate Answer
    if not results:
        return QueryResponse(answer="No relevant documents found.", citations=[])
        
    context_chunks = [res["doc"]["text"] for res in results]
    
    try:
        answer = generate_answer(request.question, context_chunks)
    except Exception as e:
        # Graceful degradation
        answer = "I encountered an error generating the answer."
        import traceback
        print(f"LLM Error: {e}")
        traceback.print_exc()

    # 4. Format Citations
    citations = []
    for res in results:
        doc = res["doc"]
        score = res["score"]
        citations.append(Citation(
            source_file=doc["metadata"]["source"],
            text_snippet=doc["text"][:200] + "...",
            chunk_id=doc["metadata"]["chunk_id"],
            score=score
        ))
        
    return QueryResponse(answer=answer, citations=citations)

@router.get("/documents", response_model=List[Document])
async def list_documents():
    # We need to aggregate chunks back to documents
    # Or just list unique sources
    # For MVP, listing unique documents from the store
    unique_docs = {}
    for doc in vector_store.documents:
        source = doc["metadata"]["source"]
        doc_id = doc["metadata"]["doc_id"]
        if doc_id not in unique_docs:
            unique_docs[doc_id] = {
                "id": doc_id,
                "filename": source,
                "upload_date": "Unknown", # We didn't store formatted date in metadata... logic gap
                "chunk_count": 0
            }
            # Try to recover timestamp from doc_id if it's what we used
            try:
                ts = int(doc_id)
                unique_docs[doc_id]["upload_date"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ts))
            except:
                pass
                
        unique_docs[doc_id]["chunk_count"] += 1
        
    return list(unique_docs.values())

@router.delete("/documents/{file_id}")
async def delete_document(file_id: str):
    success = vector_store.delete_document(file_id)
    if not success:
        raise HTTPException(status_code=404, detail="Document not found")
    return {"message": "Document deleted successfully"}

@router.get("/health", response_model=HealthResponse)
async def health_check():
    # Backend is running if we are here
    backend_status = "ok"
    
    # Storage check
    try:
        if vector_store:
            storage_status = "ok"
        else:
            storage_status = "error"
    except:
        storage_status = "error"
        
    # LLM check
    llm_status = "ok" if check_connection() else "error"
    
    return HealthResponse(
        backend=backend_status,
        storage=storage_status,
        gemini=llm_status
    )
