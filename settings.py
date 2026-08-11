import os

from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL", "https://api.demoblaze.com")
TIMEOUT = int(os.getenv("TIMEOUT", "10"))
RETRY_ATTEMPTS = int(os.getenv("RETRY_ATTEMPTS", "3"))
