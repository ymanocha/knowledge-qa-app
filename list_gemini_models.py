import sys
sys.path.insert(0, 'backend')
from google import genai
from app.core.config import get_settings

settings = get_settings()
client = genai.Client(api_key=settings.GOOGLE_API_KEY)

print("Listing available models:")
for model in client.models.list():
    print(f"Name: {model.name}, Supported Methods: {model.supported_methods}")
