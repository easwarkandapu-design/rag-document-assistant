import os
from dotenv import load_dotenv
load_dotenv()
required = ["GEMINI_API_KEY", "DATABASE_URL"]
for key in required:
    print(f"{key}: {'configured' if os.getenv(key) else 'MISSING'}")
