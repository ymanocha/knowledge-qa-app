import re

def clean_text(text: str) -> str:
    """Remove null bytes and normalize whitespace."""
    text = text.replace('\0', '')
    return re.sub(r'\s+', ' ', text).strip()

def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:
    """
    Chunk text with sliding window.
    Prioritizes splitting on double newlines, then single newlines.
    """
    chunks = []
    start = 0
    text_len = len(text)

    while start < text_len:
        end = min(start + chunk_size, text_len)
        
        # Try to find a nice break point if we are not at the very end
        if end < text_len:
            chunk_candidate = text[start:end]
            last_newline = chunk_candidate.rfind('\n')
            
            # Only split if the newline is in the latter half of the chunk
            # and ensures the chunk is at least bigger than overlap
            if last_newline != -1 and last_newline > chunk_size * 0.5:
                end = start + last_newline + 1
        
        chunk = text[start:end]
        chunks.append(chunk)
        
        # Calculate step size
        step = len(chunk) - overlap
        
        # CRITICAL FIX: Ensure we always move forward by at least 1 character
        # If the chunk is smaller than overlap (e.g. at end of file), just move by len(chunk)
        if step <= 0:
            start += len(chunk)
        else:
            start += step
            
    return chunks
