import os


BOT_TOKEN = os.getenv("BOT_TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL")
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
MAX_INPUT_MB = int(os.getenv("MAX_INPUT_MB", "50"))
OPEN_ROUTER_KEY = os.getenv("OPEN_ROUTER_KEY")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "openai/gpt-4o-mini")
