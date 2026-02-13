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

"Create Gemini API wrapper for text-embedding-004 (embeddings) and gemini-1.5-flash (chat completion)"

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
"Implement session isolation for privacy:
- Frontend should generate a UUID and store it in sessionStorage
- Add X-Session-ID header to all API requests (upload, query, get documents, delete)
- Backend needs to validate this header is present, reject requests without it
- Store session_id with each document chunk in the vector store
- Filter all searches and retrievals by session_id so users only see their own documents
- Handle backward compatibility - if old documents don't have session_id, ignore them safely
- Make sure this doesn't crash if storage.json has legacy documents
- Keep it simple, no authentication system needed, just session separation"

"Add a helper function to extract and validate session_id from headers instead of duplicating code in each route"

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
- **Direct Gemini API** for transparency and simplicity
- **In-memory storage with JSON persistence** for demo purposes
- **Session-based isolation** using UUID headers for privacy without authentication
- **Render + Vercel** for free hosting
- **gemini-1.5-flash** for chat completion (fast and cost-effective)
- **text-embedding-004** for embeddings