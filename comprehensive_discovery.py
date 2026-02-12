import sys
sys.path.insert(0, 'backend')
from google import genai
from app.core.config import get_settings
import time

settings = get_settings()
client = genai.Client(api_key=settings.GOOGLE_API_KEY)

print("Listing all available models from client:")
with open('comprehensive_models.txt', 'w') as f:
    for model in client.models.list():
        f.write(f"{model.name}\n")
        print(model.name)

test_models = [
    "models/gemini-2.0-flash",
    "models/gemini-1.5-flash",
    "gemini-2.0-flash",
    "gemini-1.5-flash",
    "models/gemini-pro",
    "gemini-pro"
]

print("\nTesting connectivity:")
for m in test_models:
    try:
        print(f"Testing {m}...", end=" ", flush=True)
        resp = client.models.generate_content(model=m, contents="hi")
        print("OK")
    except Exception as e:
        print(f"FAIL: {str(e)[:100]}")
    time.sleep(1)
