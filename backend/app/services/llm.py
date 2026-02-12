from google import genai
from google.genai import types
from app.core.config import get_settings
from typing import List
import time
import logging

settings = get_settings()
client = genai.Client(api_key=settings.GOOGLE_API_KEY)
logger = logging.getLogger(__name__)

def get_embedding(text: str) -> List[float]:
    """Generates embedding for the given text using the configured model."""
    text = text.replace("\n", " ")
    
    max_retries = 3
    for attempt in range(max_retries):
        try:
            result = client.models.embed_content(
                model=settings.EMBEDDING_MODEL,
                contents=text
            )
            return result.embeddings[0].values
        except Exception as e:
            if "429" in str(e) and attempt < max_retries - 1:
                wait_time = (attempt + 1) * 2
                logger.warning(f"Embedding rate limit hit, retrying in {wait_time}s...")
                time.sleep(wait_time)
                continue
            raise e

def generate_answer(query: str, context_chunks: List[str]) -> str:
    """Generates an answer based on the query and retrieved context."""
    
    context_text = "\n\n---\n\n".join(context_chunks)
    
    system_instruction = """You are a helpful assistant for a Private Knowledge Q&A system.
Answer the user question based ONLY on the provided context below.
If the answer cannot be found in the context, state that you cannot find the answer in the documents.
Do not hallucinate or use outside knowledge.
"""

    user_message = f"""Context:
{context_text}

Question: {query}
"""

    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model=settings.CHAT_MODEL,
                contents=user_message,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    temperature=0.0
                )
            )
            return response.text
        except Exception as e:
            if "429" in str(e) and attempt < max_retries - 1:
                wait_time = (attempt + 1) * 5
                logger.warning(f"Chat rate limit hit, retrying in {wait_time}s...")
                time.sleep(wait_time)
                continue
            raise e

def check_connection() -> bool:
    try:
        # Simple test to check if we can list models
        models = client.models.list()
        # Just check if we get anything back
        return True
    except Exception:
        return False
