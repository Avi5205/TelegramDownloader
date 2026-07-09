from pathlib import Path

from config.settings import BASE_DIR

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

SRC_DIR = PROJECT_ROOT / "src"

SESSIONS_DIR = PROJECT_ROOT / "sessions"
DOWNLOADS_DIR = PROJECT_ROOT / "downloads"
LOGS_DIR = PROJECT_ROOT / "logs"
RESOURCES_DIR = PROJECT_ROOT / "resources"

for directory in (
        SESSIONS_DIR,
        DOWNLOADS_DIR,
        LOGS_DIR,
        RESOURCES_DIR,
):
    directory.mkdir(parents=True, exist_ok=True)

# --- Database paths ---
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

DB_PATH = DATA_DIR / "telegram_downloader.db"
