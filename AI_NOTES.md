# AI Notes

## AI Tools Used
- **Cursor/Agent**: Used for:
    - Scaffolding the FastAPI backend and React frontend.
    - Implementing the `SimpleVectorStore` with explicit cosine similarity.
    - Generating the `Sidebar` and `ChatInterface` components with Tailwind styling.
- **LLM (Runtime)**: 
    - `models/text-embedding-004`: Chosen for low latency and Google Gemini integration.
    - `gemini-1.5-flash`: Chosen for speed, high-quality reasoning, and free-tier accessibility.

## Manual Verification & Safeguards
- [x] **Math Check**: Implemented explicit Cosine Similarity formula: `np.dot(a, b) / (norm(a) * norm(b))`.
- [x] **Security**: 
    - File Upload: Added checks for `.txt` extension, MIME type, max size (10MB), and null bytes (binary prevention).
    - Prompt Injection: System prompt instructs the model to Answer ONLY based on context.
- [x] **Citations**: 
    - Frontend renders exact text snippets and confidence scores.
    - Backend explicitly maps chunks to source filenames.

## Implementation Decisions
- **Gemini Migration**: Switched from OpenAI to Google Gemini to utilize the free tier for development.
- **Why no LangChain?**: 
    - To keep the stack lightweight and debuggable.
    - To demonstrate understanding of the RAG pipeline (Chunking -> Embedding -> Retrieval -> Generation).
- **Why In-Memory Store?**: 
    - For <100 documents, O(N) search is negligible (<10ms).
    - Removes infrastructure complexity (no need for Pinecone/Chroma server).
    - Persistence via `storage.json` allows restart recovery (on local disk).
