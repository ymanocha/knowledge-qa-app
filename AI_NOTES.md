# AI Usage Notes

## AI Tool Used

**Antigravity (Google DeepMind)** - Used for code generation, debugging, and implementation guidance throughout development.

## What AI Was Used For

- Project structure setup (FastAPI routes, React components)
- RAG implementation (chunking, embeddings, cosine similarity)
- API endpoints with validation
- Frontend components (upload, chat, citations, status page)
- CORS configuration
- Session isolation implementation
- Deployment configuration (Render, Vercel)

## What I Checked/Verified Myself

- Tested file upload and Q&A functionality manually
- Debugged CORS issues between Vercel and Render
- Fixed route 404 errors (missing /api prefix)
- Discovered session isolation issue during cross-device testing
- Verified citations show text snippets, not just filenames
- Tested cold start behavior on Render
- Checked error messages display properly
- Verified session isolation works across laptop and phone

## Problems I Found

1. **Session privacy bug** - Discovered documents appeared across devices, specified requirements for X-Session-ID isolation
2. **CORS errors** - Debugged origin mismatch between localhost and production
3. **Route 404s** - Identified missing API prefix through production logs
4. **Intermittent failures** - Tested and confirmed Render cold start pattern

## LLM Choice

### Embeddings: `text-embedding-004`
Google's embedding model for document similarity.

### Chat: `gemini-1.5-flash-latest`
**Why chosen:**
- Fast response times for real-time Q&A
- Large context window (1M tokens) handles multiple chunks
- Cost-effective for demo
- Single provider (Google) simplifies API key management

## Summary

AI handled code generation and implementation. I handled testing, bug discovery, debugging production issues, and specifying requirements (especially for session isolation feature).