# Private Knowledge Q&A System

RAG-based document Q&A application with session isolation.

## How to Run

### Backend
```bash
cd backend
pip install -r requirements.txt
# Create .env with GOOGLE_API_KEY
uvicorn app.main:app --reload
```

### Frontend
```bash
cd frontend
npm install
# Create .env with VITE_API_URL=http://localhost:8000/api
npm run dev
```

## What is Done

- Document upload (.txt files, max 10MB, limit 5 per session)
- Text chunking (500 chars, 50 char overlap)
- RAG pipeline with Google Gemini (text-embedding-004 + gemini-1.5-flash)
- Q&A with citations (shows source file, snippet, similarity score)
- Session isolation using X-Session-ID header
- Health monitoring page
- Deployed to Render (backend) + Vercel (frontend)

## What is Not Done

- Persistent database (uses in-memory storage with JSON backup)
- User authentication (session isolation only, not secure)
- PDF/DOCX support (only .txt files)
- Document deletion UI
- Production-grade security

## Live Links

- Frontend: https://knowledge-qa-app.vercel.app
- Backend: https://knowledge-qa-app.onrender.com

## Notes

This is a demo project. Render free tier has cold starts (~30-60s) and ephemeral storage (data resets on redeploy).