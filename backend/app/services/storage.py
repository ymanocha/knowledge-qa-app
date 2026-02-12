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

    def add(self, text: str, vector: List[float], metadata: Dict):
        doc = {
            "id": len(self.documents),
            "text": text,
            "vector": vector,
            "metadata": metadata
        }
        self.documents.append(doc)
        self.save()

    def search(self, query_vector: List[float], k: int = 3) -> List[Dict]:
        if not self.documents:
            return []

        # Convert query list to numpy array and normalize
        q_vec = np.array(query_vector)
        q_norm = np.linalg.norm(q_vec)
        if q_norm == 0:
            return []
        
        results = []
        for doc in self.documents:
            d_vec = np.array(doc["vector"])
            d_norm = np.linalg.norm(d_vec)
            
            if d_norm == 0:
                score = 0
            else:
                # Cosine Similarity: (A . B) / (||A|| * ||B||)
                score = np.dot(q_vec, d_vec) / (q_norm * d_norm)
            
            results.append({
                "doc": doc,
                "score": float(score)
            })
        
        # Sort by score descending
        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:k]

    def save(self):
        # We need to serialize numpy arrays/lists
        # But vector is already stored as list in add() if passed as list?
        # Let's ensure consistency.
        # Ideally, we don't save vectors to JSON if they are large, but for this scale it's fine.
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

    def delete_document(self, doc_id: str):
        """Removes all chunks associated with a doc_id."""
        initial_count = len(self.documents)
        self.documents = [doc for doc in self.documents if doc.get("metadata", {}).get("doc_id") != doc_id]
        if len(self.documents) < initial_count:
            self.save()
            return True
        return False

# Global instance
vector_store = SimpleVectorStore()
