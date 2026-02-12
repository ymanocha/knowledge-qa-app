import requests
import json

BASE_URL = "http://localhost:8000/api"

def test_deletion():
    # 1. Get documents
    resp = requests.get(f"{BASE_URL}/documents")
    docs = resp.json()
    if not docs:
        print("No documents to delete. Upload one first.")
        return
    
    doc_to_delete = docs[0]
    doc_id = doc_to_delete['id']
    filename = doc_to_delete['filename']
    print(f"Deleting document: {filename} (ID: {doc_id})")
    
    # 2. Delete document
    resp = requests.delete(f"{BASE_URL}/documents/{doc_id}")
    print(f"Delete Response: {resp.status_code} - {resp.json()}")
    
    # 3. Verify deletion
    resp = requests.get(f"{BASE_URL}/documents")
    docs_after = resp.json()
    deleted = all(d['id'] != doc_id for d in docs_after)
    print(f"Verified Deletion: {'SUCCESS' if deleted else 'FAILED'}")

if __name__ == "__main__":
    test_deletion()
