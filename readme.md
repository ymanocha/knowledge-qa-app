# Private Knowledge Q&A System

A RAG (Retrieval-Augmented Generation) system for private document querying using FastAPI, React (Vite), and Google Gemini.

## Features
- **Local Document Storage**: Upload and query `.txt` files.
- **Session Isolation**: Your data is isolated to your browser session. Laptop and mobile devices will have their own private knowledge bases.
- **Clean UI**: Modern, responsive dark-themed interface.

## Security & Privacy
> [!IMPORTANT]
> This application implements **Session Isolation** for privacy, not production-grade authentication.
>
> - Documents are isolated using a client-generated `X-Session-ID` stored in your browser's `localStorage`.
> - This prevents accidental sharing of documents between different users or devices.
> - **Note**: This design is appropriate for a take-home/personal project but can be spoofed by anyone with knowledge of your session ID. It does not use JWT or OAuth.

## Deployment
See [DEPLOYMENT.md](DEPLOYMENT.md) for instructions on hosting this for free on Render and Vercel.
