import requests

# Test query endpoint
try:
    payload = {
        "question": "What does product A have?",
        "k": 3
    }
    response = requests.post("http://localhost:8000/api/query", json=payload)
    print("Query test:", response.status_code)
    if response.status_code != 200:
        print("Error:", response.text)
    else:
        result = response.json()
        print("Answer:", result.get('answer'))
        print("Citations:", len(result.get('citations', [])))
except Exception as e:
    print(f"Query test failed: {e}")
