# Private Knowledge Q&A

A robust, AI-native full-stack application for querying private text documents. Built with FastAPI, React, and Google Gemini.

## Features
- **Secure Uploads**: rigorous validation for text files (Size, Type, Binary Content).
- **RAG Engine**: Custom in-memory vector store with explicit cosine similarity and Top-3 retrieval.
- **Precision Citations**: Answers include exact text snippets, source filenames, and confidence scores.
- **System Health**: Dedicated status page for Backend, Storage, and LLM connectivity.

## Tech Stack
- **Backend**: FastAPI, NumPy (Vector Math), Google Gemini API.
- **Frontend**: React (Vite), Tailwind CSS, Lucide React.
- **Deployment**: Render (Backend) + Vercel (Frontend).

## Quick Start (Local)

### Prerequisites
- Python 3.10+
- Node.js 18+
- Google Gemini API Key

### Backend
1. `cd backend`
2. `python -m venv venv`
3. `venv\Scripts\activate` (Windows) or `source venv/bin/activate` (Mac/Linux)
4. `pip install -r requirements.txt`
5. Copy `.env.example` to `.env` and add your `GOOGLE_API_KEY`.
6. Run server: `uvicorn app.main:app --reload`
   - API Docs: http://localhost:8000/docs

### Frontend
1. `cd frontend`
2. `npm install`
3. Create `.env` with `VITE_API_URL=http://localhost:8000/api`
4. Run app: `npm run dev`
   - App: http://localhost:5173

## Deployment Guide

### Backend (Render)
1. Create a new Web Service on Render connected to this repo.
2. Root Directory: `backend`
3. Build Command: `pip install -r requirements.txt`
4. Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Add Environment Variable: `OPENAI_API_KEY`, `PYTHON_VERSION=3.11.0`

### Frontend (Vercel)
1. Import project to Vercel.
2. Root Directory: `frontend`
3. Framework Preset: Vite
4. Add Environment Variable: `VITE_API_URL` (Your Render Backend URL + `/api`)

## Logic & Architecture
- **In-Memory Store**: Uses an efficient list of dictionaries for document storage. 
- **Cosine Similarity**: `np.dot(a, b) / (norm(a) * norm(b))` used for accurate semantic retrieval.
- **Chunking**: Sliding window (500 chars size, 50 chars overlap) to preserve context.

## Limitations
- **Persistence on Render**: The free tier of Render does not support persistent disks. `storage.json` will be wiped on every deployment or restart.
- **File Support**: Currently restricted to `.txt` files for security and simplicity.
