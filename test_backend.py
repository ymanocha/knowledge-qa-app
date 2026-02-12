import requests

# Test health endpoint
try:
    response = requests.get("http://localhost:8000/api/health")
    print("Health check:", response.status_code)
    print(response.json())
except Exception as e:
    print(f"Health check failed: {e}")

# Test upload with a simple text file
try:
    files = {'file': ('test.txt', 'This is a test document for the knowledge base.', 'text/plain')}
    response = requests.post("http://localhost:8000/api/upload", files=files)
    print("\nUpload test:", response.status_code)
    if response.status_code != 200:
        print("Error:", response.text)
    else:
        print(response.json())
except Exception as e:
    print(f"Upload test failed: {e}")
