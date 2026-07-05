# TGVault Architecture

## Overview

TGVault is a desktop application for discovering, filtering, and downloading files from Telegram channels. The architecture is built on **clean layering**, **dependency injection**, and **strong typing**.

---

## Layered Architecture

```
┌─────────────────────────────────────────────┐
│        PRESENTATION LAYER (Qt)              │
│  ┌──────────────────────────────────────┐   │
│  │ MainWindow (Orchestrator)            │   │
│  │  ├── FileTableWidget (Presentation)  │   │
│  │  ├── ChannelDetailsWidget            │   │
│  │  └── StatusBar / Dialogs             │   │
│  └──────────────────────────────────────┘   │
└──────────────────┬──────────────────────────┘
                   │
┌──────────────────▼──────────────────────────┐
│      APPLICATION LAYER (Services)           │
│  ┌──────────────────────────────────────┐   │
│  │ TelegramScanner                      │   │
│  │ DownloadManager                      │   │
│  │ Repositories (Channel, File, etc.)   │   │
│  └──────────────────────────────────────┘   │
└──────────────────┬──────────────────────────┘
                   │
┌──────────────────▼──────────────────────────┐
│        DOMAIN LAYER (Models)                │
│  ┌──────────────────────────────────────┐   │
│  │ Channel, FileInfo, ScanResult        │   │
│  │ DownloadResult, DownloadProgress     │   │
│  │ (Pure business logic, no side fx)    │   │
│  └──────────────────────────────────────┘   │
└──────────────────┬──────────────────────────┘
                   │
┌──────────────────▼──────────────────────────┐
│    INFRASTRUCTURE LAYER (External APIs)     │
│  ┌──────────────────────────────────────┐   │
│  │ TelegramService (Telethon wrapper)   │   │
│  │ Database (SQLite) — v0.2.0+          │   │
│  └──────────────────────────────────────┘   │
└─────────────────────────────────────────────┘
```

---

## Design Principles

### 1. Dependency Inversion

Dependencies always flow **inward** toward the domain:

```
UI → Services → Domain ← Infrastructure
```

The domain layer has **zero dependencies** on frameworks.

### 2. Single Responsibility

Each class has one reason to change:

- `FileTableModel` → Data representation
- `FileTableWidget` → Presentation
- `FileFilterProxyModel` → Filtering/sorting
- `TelegramScanner` → Scan orchestration
- `TelegramService` → Telethon abstraction

### 3. Separation of Concerns

- **UI doesn't execute queries** → Use repositories
- **Application doesn't know about Telethon** → Use services
- **Domain doesn't depend on frameworks** → Pure dataclasses

### 4. Composition Over Inheritance

- Use composition (e.g., `MainWindow` owns models)
- Avoid deep inheritance hierarchies
- Inject dependencies explicitly

---

## Key Components

### MainWindow (Presentation Orchestrator)

Coordinates all UI interactions. Doesn't execute business logic directly; delegates to services.

```python
class MainWindow(QMainWindow):
    def __init__(self, scanner: TelegramScanner, download_manager: DownloadManager):
        self._scanner = scanner
        self._download_manager = download_manager
        # Creates and owns models
        self._file_model = FileTableModel()
        self._file_proxy = FileFilterProxyModel(self._file_model)
```

### TelegramService (Infrastructure)

Wraps Telethon and provides a clean API to the application layer.

```python
class TelegramService:
    async def connect()
    async def me()
    async def get_channels()
    async def get_messages(channel_id, limit)
    async def download_media(file_info, destination)
```

### TelegramScanner (Application Service)

Orchestrates channel scanning. Decoupled from Telethon.

```python
class TelegramScanner:
    async def scan_channel(channel_id) -> ScanResult
```

### DownloadManager (Application Service)

Orchestrates file downloads. Manages progress callbacks and result aggregation.

```python
class DownloadManager:
    async def download(files, destination, progress_callback) -> DownloadResult
```

### Domain Models

Pure dataclasses with no dependencies:

```python
@dataclass
class Channel:
    id: int
    title: str
    username: str

@dataclass
class FileInfo:
    id: int
    name: str
    size: int
    category: str
```

---

## Async Architecture

TGVault uses `qasync` to run async Python code in the Qt event loop.

- **Long operations** (scanning, downloading) run as `asyncio.Task` objects.
- **UI stays responsive** during I/O.
- **Progress callbacks** update the UI from async tasks.
- **Tasks are tracked** to prevent concurrent duplicate operations.

---

## Testing Strategy

Each layer has corresponding tests:

- **Unit tests** for domain models (no mocking needed).
- **Unit tests** for services (mock infrastructure).
- **Integration tests** for repositories.
- **UI tests** for widgets (mock services).

---

## Future Evolution

As TGVault grows:

1. **v0.2.0**: Add SQLite persistence (respects layered architecture).
2. **v0.3.0**: Download queue and resume (services layer).
3. **v0.4.0**: Settings and preferences (UI + application layer).
4. **v1.0.0**: Installer, auto-update, documentation.

The architecture supports all of this without major restructuring.

---

## See Also

- [ADR-001: Clean Layered Architecture](decisions/ADR-001-clean-architecture.md)
- [ADR-002: Single TelegramService Instance](decisions/ADR-002-single-telegram-service.md)
- [ADR-003: Qt Model-View Pattern](decisions/ADR-003-qt-model-view.md)
- [Roadmap](roadmap.md)
- [Database Schema (v0.2.0)](database/schema.md)
