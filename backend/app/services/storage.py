import json
import os
import numpy as np
from typing import List, Dict
from app.core.config import get_settings

settings = get_settings()

class SimpleVectorStore:
    def __init__(self):
        self.documents: List[Dict] = []
        self.storage_file = settings.STORAGE_FILE
        self.load()

    def add(self, text: str, vector: List[float], source: str, session_id: str):
        doc = {
            "id": len(self.documents),
            "text": text,
            "vector": vector,
            "source": source,
            "session_id": session_id
        }
        self.documents.append(doc)
        self.save()

    def search(self, query_vector: List[float], session_id: str, k: int = 3) -> List[Dict]:
        if not self.documents:
            return []

        # Filter by session_id first (Retreival Safety)
        # Ignores legacy documents without session_id
        user_docs = [doc for doc in self.documents if doc.get("session_id") == session_id]
        
        if not user_docs:
            return []

        q_vec = np.array(query_vector)
        q_norm = np.linalg.norm(q_vec)
        if q_norm == 0:
            return []
        
        results = []
        for doc in user_docs:
            d_vec = np.array(doc["vector"])
            d_norm = np.linalg.norm(d_vec)
            
            if d_norm == 0:
                score = 0
            else:
                score = np.dot(q_vec, d_vec) / (q_norm * d_norm)
            
            results.append({
                "doc": doc,
                "score": float(score)
            })
        
        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:k]

    def save(self):
        with open(self.storage_file, 'w') as f:
            json.dump(self.documents, f)

    def load(self):
        if os.path.exists(self.storage_file):
            try:
                with open(self.storage_file, 'r') as f:
                    self.documents = json.load(f)
            except Exception as e:
                print(f"Error loading storage: {e}")
                self.documents = []

    def delete_document(self, doc_id: str, session_id: str):
        """Removes all segments associated with a doc_id if session_id matches."""
        initial_count = len(self.documents)
        # doc_id was stored in metadata in previous version, let's look both places for safety
        self.documents = [
            doc for doc in self.documents 
            if not (
                (doc.get("session_id") == session_id) and 
                (str(doc.get("id")) == doc_id or doc.get("metadata", {}).get("doc_id") == doc_id)
            )
        ]
        if len(self.documents) < initial_count:
            self.save()
            return True
        return False

# Global instance
vector_store = SimpleVectorStore()
