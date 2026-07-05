from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

SRC_DIR = PROJECT_ROOT / "src"

SESSIONS_DIR = PROJECT_ROOT / "sessions"
DOWNLOADS_DIR = PROJECT_ROOT / "downloads"
DATABASE_DIR = PROJECT_ROOT / "database"
LOGS_DIR = PROJECT_ROOT / "logs"
RESOURCES_DIR = PROJECT_ROOT / "resources"

for directory in (
        SESSIONS_DIR,
        DOWNLOADS_DIR,
        DATABASE_DIR,
        LOGS_DIR,
        RESOURCES_DIR,
):
    directory.mkdir(parents=True, exist_ok=True)
