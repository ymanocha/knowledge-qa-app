import sys
sys.path.insert(0, 'backend')
from google import genai
from app.core.config import get_settings

settings = get_settings()
client = genai.Client(api_key=settings.GOOGLE_API_KEY)

print("Listing available models:")
try:
    for model in client.models.list():
        print(f"Name: {model.name}")
except Exception as e:
    print(f"Error: {e}")
