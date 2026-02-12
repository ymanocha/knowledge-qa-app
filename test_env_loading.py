import sys
import os
sys.path.insert(0, 'backend')

# Check if .env file exists
env_path = 'backend/.env'
print(f".env file exists: {os.path.exists(env_path)}")
print(f".env file content:")
with open(env_path, 'r') as f:
    print(f.read())

# Try loading settings
try:
    from app.core.config import get_settings
    settings = get_settings()
    print(f"\nSettings loaded successfully!")
    print(f"GOOGLE_API_KEY: {settings.GOOGLE_API_KEY[:20]}..." if settings.GOOGLE_API_KEY else "GOOGLE_API_KEY is None")
except Exception as e:
    import traceback
    print(f"\nError loading settings: {e}")
    traceback.print_exc()
