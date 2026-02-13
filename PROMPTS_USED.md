# Prompts Used

This file documents the key prompts used during application development, organized chronologically by development phase.

---

## Phase 1: Initial Setup & Core Development

### Project Structure
"Create a FastAPI backend structure with routes, services, and models folders for a RAG-based Q&A application"

"Set up React Vite project with Tailwind CSS and component structure for document upload and chat interface"

### Backend Implementation
"Implement text chunking function with 500 character chunks and 50 character overlap, splitting on paragraph boundaries"

"Write cosine similarity function with normalized vectors using numpy for document retrieval"

"Create OpenAI API wrapper for text-embedding-3-small (embeddings) and gpt-4o-mini (chat completion)"

### Frontend Components
"Build UploadDropzone component with drag-and-drop file upload and client-side validation"

"Create ChatInterface component with message history, loading states, and citation display"

"Build CitationBlock component showing source file, text snippet, and similarity score"

---

## Phase 2: CORS & Deployment Issues

### CORS Configuration
"Fix CORS error between localhost:5173 (Vite) and localhost:8000 (FastAPI)"

"This is vercel environment vite_api_url = https://knowledge-qa-app.onrender.com/api and this is vercel domain: https://knowledge-qa-app.vercel.app/ and this is render domain: https://knowledge-qa-app.onrender.com and this is its environment variable. ALLOWED_ORIGINS = https://knowledge-qa-app.vercel.app ? what am i doing wrong its not working"

### Endpoint Issues
"Getting 404 errors on POST /upload endpoint in production. Backend logs show:
```
INFO: 103.211.12.27:0 - "POST /upload HTTP/1.1" 404 Not Found
```
Frontend is calling /upload but route expects /api/upload"

### Intermittent Failures
"I added both the urls and refreshed and the file got uploaded and worked also it shows the backend operational but when i deleted the file and tried it again it again stopped working but the backend still shows operational and now its not working but i have noticed a pattern. if i leave it as it is that says not found and i refresh it sometimes it works but many times doesnt"

---

## Phase 3: Session Isolation Feature

### Problem Discovery
"The upload works correctly but i think there is a major issue. when i upload it on pc and refresh the site on my phone it comes up also on my phone. shouldnt it be private sessions? why can i see my laptops uploaded file on my phone"

### Implementation Requirements
"Your session isolation proposal is directionally correct but incomplete and has architectural gaps.

Please refine the implementation plan with the following corrections and constraints.

CONTEXT:
The current system uses a global in-memory vector store. We are introducing session-level isolation using a frontend-generated UUID passed via X-Session-ID header.

DO NOT:
- Add authentication systems (no JWT, no login, no OAuth)
- Add databases
- Add external services
- Expand scope beyond session isolation
- Increase overall complexity

STRICT REQUIREMENTS TO FIX:

1️⃣ Enforce Session ID Presence
- All relevant routes MUST reject requests missing X-Session-ID with HTTP 400
- Add a reusable helper function for extracting and validating session_id

2️⃣ Update ALL Relevant Routes
Include: POST /upload, POST /query, GET /documents, DELETE /documents/{file_id}

3️⃣ Define Explicit Data Structure
{
  "id": int,
  "text": str,
  "vector": list,
  "source": str,
  "session_id": str
}

4️⃣ Retrieval Safety
- Filter documents by session_id BEFORE cosine similarity
- Use safe access (doc.get("session_id")) to avoid crashes
- Maintain Top-K = 3 logic

5️⃣ JSON Persistence Backward Compatibility
- Handle legacy records without session_id safely
- No crashes allowed

6️⃣ README Clarification
- State this is session isolation, not authentication
- X-Session-ID can be spoofed
- Appropriate for take-home, not production-grade security

7️⃣ Keep It Lightweight
- Implementable in under 1-1.5 hours"

---

## Phase 4: Documentation & Finalization

### Documentation Improvements
"Help me improve these files:
* A short README: how to run, what is done, what is not done
* A short AI_NOTES.md: what you used AI for, and what you checked yourself. Which LLM and provider does your app use and why
* Put your name and resume in ABOUTME.md
* A PROMPTS_USED.md, with records of your prompts used for app development"

---

## Technical Decisions Made

Throughout development, the following key technical choices were made:
- **Direct OpenAI API** over LangChain for transparency and simplicity
- **In-memory storage with JSON persistence** for demo purposes
- **Session-based isolation** using UUID headers for privacy without authentication
- **Render + Vercel** for free hosting over Docker deployment
- **gpt-4o-mini** for chat completion (cost-effective with good quality)
- **text-embedding-3-small** for embeddings (fast and efficient)