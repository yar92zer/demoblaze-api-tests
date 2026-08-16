import os

from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL", "https://api.demoblaze.com")
FRONT_URL = os.getenv("FRONT_URL", "https://www.demoblaze.com")
TIMEOUT = int(os.getenv("TIMEOUT", "30"))
RETRY_ATTEMPTS = int(os.getenv("RETRY_ATTEMPTS", "3"))
