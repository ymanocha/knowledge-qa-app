import sys
sys.path.insert(0, 'backend')

from app.services.llm import generate_answer

try:
    context = ["Product A: Features a 5000mAh battery. Released in 2024."]
    answer = generate_answer("What does product A have?", context)
    print(f"Success! Answer: {answer}")
except Exception as e:
    import traceback
    print(f"Error: {e}")
    traceback.print_exc()
