#!/bin/bash

set -e

echo "========================================="
echo " Telegram Downloader Bootstrap"
echo "========================================="

PROJECT_ROOT=$(pwd)

echo "Project Root: $PROJECT_ROOT"

echo ""
echo "Creating required directories..."

mkdir -p sessions
mkdir -p downloads
mkdir -p logs
mkdir -p database
mkdir -p resources
mkdir -p tests

echo "Directories created."

echo ""
echo "Checking virtual environment..."

if [ ! -d ".venv" ]; then
    echo "Creating Python virtual environment..."
    /opt/homebrew/bin/python3.13 -m venv .venv
fi

source .venv/bin/activate

echo ""
echo "Upgrading pip..."

python -m pip install --upgrade pip

echo ""
echo "Installing requirements..."

if [ -f "requirements.txt" ]; then
    python -m pip install -r requirements.txt
fi

echo ""
echo "Creating .env if missing..."

if [ ! -f ".env" ]; then
cat > .env <<EOF
API_ID=
API_HASH=
SESSION_NAME=telegram_downloader
EOF
fi

echo ""
echo "Creating config/paths.py..."

mkdir -p src/config

cat > src/config/paths.py <<EOF
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
EOF

echo ""
echo "Creating utils/logger.py..."

mkdir -p src/utils

cat > src/utils/logger.py <<EOF
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)

logger = logging.getLogger("telegram_downloader")
EOF

echo ""
echo "Checking PyCharm project..."

mkdir -p .idea

echo ""
echo "Environment"

python --version

echo ""
echo "Python Executable"

which python

echo ""
echo "Project Structure"

find . -maxdepth 2 -type d

echo ""
echo "========================================="
echo " Bootstrap Completed Successfully"
echo "========================================="

echo ""
echo "Next Steps"
echo ""
echo "1. Open PyCharm"
echo "2. File -> Open -> TelegramDownloader"
echo "3. Settings -> Python Interpreter -> .venv"
echo "4. Run Configuration:"
echo "       Script : src/main.py"
echo "       Working Directory : $PROJECT_ROOT"
echo ""
echo "Run:"
echo ""
echo "python src/main.py"