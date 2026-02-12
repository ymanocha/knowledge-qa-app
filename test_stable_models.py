import sys
sys.path.insert(0, 'backend')
from google import genai
from app.core.config import get_settings
import time

settings = get_settings()
client = genai.Client(api_key=settings.GOOGLE_API_KEY)

models_to_try = ['models/gemini-flash-latest', 'models/gemini-2.0-flash', 'models/gemini-2.5-flash']

for m in models_to_try:
    print(f"Testing {m}:", end=" ", flush=True)
    try:
        resp = client.models.generate_content(model=m, contents="hi")
        print(f"OK - Response: {resp.text}")
    except Exception as e:
        print(f"FAILED: {e}")
    time.sleep(2)
