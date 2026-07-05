# TGVault

> A modern desktop application for browsing, searching, and downloading media from Telegram channels and groups.

![Python](https://img.shields.io/badge/Python-3.13-blue)
![Qt](https://img.shields.io/badge/PySide6-6.x-green)
![Telethon](https://img.shields.io/badge/Telethon-Latest-blue)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## Overview

TGVault is a desktop application built with **PySide6** and **Telethon** that allows you to:

- Browse all your Telegram channels and groups
- Scan media without downloading it
- Search and filter files instantly
- View metadata such as:
  - File name
  - Size
  - Category
  - Date
- Download selected files to your local machine

The application follows a clean layered architecture and is designed to scale with future features such as persistence, download queues, resume support, and advanced search.

---

# Features

## Current Features (v0.1.0 Alpha)

- Telegram Login (Telethon Session)
- Browse Channels & Groups
- Scan Media
- File Metadata Extraction
- Search Files
- Category Filtering
- Download Selected Files
- Async UI (No Freezing)
- Model/View Qt Architecture
- Clean Architecture
- Dependency Injection
- SOLID Principles

---

# Screenshots

> *(Add screenshots here later)*

```
Login
↓

Load Channels
↓

Scan

↓

Browse Files

↓

Download
```

---

# Tech Stack

| Layer | Technology |
|---------|------------|
| Language | Python 3.13 |
| GUI | PySide6 |
| Telegram API | Telethon |
| Async Runtime | asyncio + qasync |
| Architecture | Clean Architecture |
| Design | SOLID |
| Pattern | Repository Pattern |
| Pattern | Dependency Injection |
| Pattern | Model/View (Qt) |

---

# Project Structure

```
TelegramDownloader/

│
├── src/
│
│   ├── config/
│   ├── database/
│   ├── download/
│   ├── models/
│   ├── telegram/
│   ├── ui/
│   ├── utils/
│   └── main.py
│
├── tests/
│
├── docs/
│
├── resources/
│
├── requirements.txt
├── README.md
└── CHANGELOG.md
```

---

# Prerequisites

Before starting, ensure the following software is installed.

## Python

Python **3.13** or newer

Verify:

```bash
python --version
```

Example

```
Python 3.13.4
```

---

## Git

```bash
git --version
```

---

## Telegram API Credentials

Create your own Telegram API credentials.

Visit:

https://my.telegram.org

Navigate to

```
API Development Tools
```

Create an application.

You will receive:

```
API_ID

API_HASH
```

These are required.

---

# Installation

## Clone Repository

```bash
git clone https://github.com/Avi5205/TelegramDownloader.git

cd TelegramDownloader
```

---

## Create Virtual Environment

macOS / Linux

```bash
python3.13 -m venv .venv
```

Windows

```bash
python -m venv .venv
```

---

## Activate Environment

macOS

```bash
source .venv/bin/activate
```

Windows

```bash
.venv\Scripts\activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Environment Configuration

Copy

```text
.env.example
```

to

```text
.env
```

Example

```env
API_ID=1234567

API_HASH=xxxxxxxxxxxxxxxxxxxxxxxx

SESSION_NAME=telegram_downloader
```

---

# Verify Installation

Ensure

```
Python 3.13
```

```
PySide6
```

```
Telethon
```

are installed.

Run

```bash
pip list
```

You should see

```
PySide6

Telethon

qasync
```

---

# Running the Application

```bash
python src/main.py
```

On first launch

1. Telegram asks for your phone number.
2. Enter OTP.
3. Session is stored locally.
4. Future launches won't ask again.

---

# First Scan

1. Open application

2. Select a channel

3. Click

```
Scan Channel
```

4. Wait for scan completion

5. Browse files

6. Select files

7. Click

```
Download Selected
```

8. Choose download directory

---

# Project Workflow

```
Login

↓

Load Channels

↓

Scan Channel

↓

Browse Files

↓

Search

↓

Filter

↓

Select Files

↓

Download
```

---

# Development

## Run Tests

```bash
pytest
```

---

## Format Code

```bash
black .
```

---

## Lint

```bash
ruff check .
```

---

## Type Checking

```bash
mypy src
```

---

# Engineering Standards

The project follows:

- SOLID Principles
- Clean Architecture
- Repository Pattern
- Dependency Injection
- Qt Model/View
- Conventional Commits
- GitHub Flow

See

```
docs/
```

for

- Architecture
- Engineering Principles
- ADRs
- Roadmap
- Database Design

---

# Roadmap

## v0.1.0

- Scan
- Download
- Search
- Filter

## v0.2.0

- SQLite Persistence
- Scan Cache
- Download History

## v0.3.0

- Resume Downloads
- Retry
- Parallel Queue

## v0.4.0

- File Preview
- Export Metadata

## v1.0.0

- Installer
- Auto Update
- Settings
- Production Release

---

# Contributing

1. Fork repository

2. Create feature branch

```
feature/my-feature
```

3. Follow Engineering Principles

4. Run tests

5. Submit Pull Request

---

# Troubleshooting

## Session Issues

Delete

```
sessions/
```

and login again.

---

## Module Not Found

Verify virtual environment is activated.

```bash
source .venv/bin/activate
```

---

## Invalid API_ID

Verify

```
.env
```

contains valid Telegram credentials.

---

## PySide6 Errors

Ensure Python 3.13 is being used.

```
python --version
```

---

# Security

Never commit

```
.env

sessions/

*.session
```

Keep API credentials private.

---

# License

MIT License

---

# Author

**Avinash Kumar**

GitHub:

https://github.com/Avi5205

---

# Acknowledgements

- Telethon
- PySide6
- Qt Framework
- Python Community

---

## Current Status

**Version**

```
v0.1.0 Alpha
```

Production Features

- Scan Telegram Channels
- Browse Files
- Download Files

Next Milestone

```
v0.2.0
SQLite Persistence
```