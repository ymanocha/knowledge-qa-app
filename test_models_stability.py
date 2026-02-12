import sys
sys.path.insert(0, 'backend')
from google import genai
from app.core.config import get_settings
import time

settings = get_settings()
client = genai.Client(api_key=settings.GOOGLE_API_KEY)

test_models = [
    "gemini-2.0-flash",
    "gemini-1.5-flash",
    "gemini-1.5-flash-8b",
    "gemini-1.5-pro",
    "gemini-2.0-flash-exp"
]

print("Testing models for connectivity and quota:")
for model_name in test_models:
    print(f"\n--- Testing {model_name} ---")
    try:
        response = client.models.generate_content(
            model=model_name,
            contents="Say 'OK' if you can hear me."
        )
        print(f"Success! Response: {response.text}")
    except Exception as e:
        print(f"Failed: {e}")
    time.sleep(1) # Avoid spamming
