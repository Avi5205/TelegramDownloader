from pathlib import Path
import os

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent.parent

load_dotenv(BASE_DIR / ".env")

API_ID = int(os.getenv("API_ID"))

API_HASH = os.getenv("API_HASH")

SESSION_NAME = os.getenv(
    "SESSION_NAME",
    "telegram_downloader",
)