# Prompts Used

*This log tracks the prompts used with AI assistants during the development of this project.*

## Planning Phase
- "Refine this implementation plan to be buildable in 6-8 hours without heavy frameworks."
- "Add explicit cosine similarity math and explicit constraints for file uploads."
- "Remove Docker as primary deployment, focus on Render/Vercel."
- "Change the code to use Gemini API keys as that is free."

## Development Phase
- "Scaffold a FastAPI project with `app/main.py`, `app/core/config.py`, and `app/models.py`."
- "Implement a simple in-memory vector store with cosine similarity using numpy."
- "Create a React component `UploadDropzone` that accepts only .txt files and validates size."
- "Create a sidebar component using Tailwind CSS that lists documents."
- "Implement a chat interface that renders markdown and shows citations."

## Refinement
- "Ensure `Sidebar` uses `Link` from `react-router-dom` instead of anchor tags."
- "Create deployment configuration files for Render (`render.yaml`) and Vercel (`vercel.json`)."
- "Migrate from OpenAI to Google Gemini for embeddings and chat completion."
