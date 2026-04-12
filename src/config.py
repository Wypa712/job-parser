import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://arbeidsplassen.nav.no/stillinger?municipal=VESTLAND.SUNNFJORD&county=VESTLAND&v=5&q=ingeni%C3%B8r"
STATE_PATH = Path("data") / "state.json"
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "groq")  # "openai" or "groq"
SCHEDULE_TIMES = ["10:00", "16:00"]
REQUEST_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/120.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}
