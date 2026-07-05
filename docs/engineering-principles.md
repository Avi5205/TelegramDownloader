# Engineering Principles

These principles guide every decision in TGVault, from architectural choices to code review.

When in doubt, return to these principles.

---

## Principle 1: Prefer Composition Over Inheritance

**What it means:**

Build complex behavior by combining simple objects, not by inheriting from complex classes.

**Example (❌ Avoid):**

```python
class TableWithSearch(QTableView):
    def search(self, query):
        # Mixing UI and search logic
        ...
```

**Example (✅ Prefer):**

```python
class FileTableWidget(QWidget):
    def __init__(self, model, proxy_model, search_box):
        self._model = model
        self._proxy_model = proxy_model
        self._search_box = search_box
        # Composed from simple parts
```

**Why:**

- Objects remain small and focused
- Behavior is explicit and testable
- Changes to one component don't cascade through inheritance hierarchy
- Composition is more flexible than inheritance

---

## Principle 2: Every Class Has One Reason to Change

**What it means:**

A class should have only one responsibility. If you can list two reasons why a class would change, refactor it.

**Example (❌ Avoid):**

```python
class FileManager:
    def download_files(self, files):
        # Reason 1: Download logic changes
        ...
    
    def save_to_database(self, files):
        # Reason 2: Database schema changes
        ...
    
    def update_ui(self, files):
        # Reason 3: UI requirements change
        ...
```

**Example (✅ Prefer):**

```python
class DownloadManager:
    async def download(self, files, destination):
        # Only reason to change: download logic
        ...

class FileRepository:
    async def save_files(self, files):
        # Only reason to change: database schema
        ...

class FileTableModel:
    def update_files(self, files):
        # Only reason to change: UI requirements
        ...
```

**Why:**

- Classes are smaller and easier to understand
- Changes are localized and less risky
- Testing is simpler (mock fewer dependencies)
- Reusability increases (one responsibility = many use cases)

---

## Principle 3: UI Never Owns Business Logic

**What it means:**

Business logic lives in services and repositories. The UI calls them; it never implements them.

**Example (❌ Avoid):**

```python
class MainWindow(QMainWindow):
    def _on_download_clicked(self):
        # ❌ Business logic in UI
        for file in self._selected_files:
            cursor = self._db.execute("SELECT ... FROM downloads WHERE file_id = ?")
            if cursor:
                continue  # Already downloaded
            await self._download(file)
```

**Example (✅ Prefer):**

```python
class MainWindow(QMainWindow):
    def _on_download_clicked(self):
        # ✅ Business logic in service
        files = self._file_table.selected_files()
        await self._download_manager.download(files, destination)
```

**Why:**

- Business logic can be tested without Qt
- Business logic can be reused in CLI, API, or other UIs
- UI changes don't affect logic
- Logic is easier to reason about (no Qt signal/slot confusion)

---

## Principle 4: Infrastructure Never Leaks Into the UI

**What it means:**

The UI should not import or directly use database, network, or file system code. Always go through a service or
repository.

**Example (❌ Avoid):**

```python
from src.database import sqlite3
from src.database.connection import Database

class MainWindow(QMainWindow):
    def __init__(self):
        self._db = Database()
        # ❌ Direct database access in UI
```

**Example (✅ Prefer):**

```python
class MainWindow(QMainWindow):
    def __init__(self, scanner: TelegramScanner, download_manager: DownloadManager):
        self._scanner = scanner
        self._download_manager = download_manager
        # ✅ Dependencies injected; no direct infrastructure
```

**Why:**

- UI layer remains independent of infrastructure choices
- Can swap SQLite for PostgreSQL without touching UI
- Testing doesn't require database setup
- Clear dependency direction (UI → Services → Infrastructure)

---

## Principle 5: Every Public Method Has Explicit Types

**What it means:**

All function signatures include type hints. No `Any`, no omitted return types.

**Example (❌ Avoid):**

```python
async def download(self, files, destination):
    # ❌ Unclear what types are accepted
    ...
```

**Example (✅ Prefer):**

```python
async def download(
    self,
    files: list[FileInfo],
    destination: Path,
) -> DownloadResult:
    # ✅ Crystal clear contract
    ...
```

**Why:**

- IDE autocomplete works better
- Static analysis catches bugs early
- Code is self-documenting
- Reduces runtime surprises
- Makes refactoring safer

---

## Principle 6: Async Code Never Blocks the UI Thread

**What it means:**

Long operations run in `asyncio.Task` objects, never on the main thread.

**Example (❌ Avoid):**

```python
def _on_scan_clicked(self):
    result = self._scanner.scan_channel(channel_id)  # ❌ Blocks UI
    self._file_table.update(result.files)
```

**Example (✅ Prefer):**

```python
def _on_scan_clicked(self):
    self._scan_task = asyncio.create_task(self._perform_scan())

async def _perform_scan(self):
    result = await self._scanner.scan_channel(channel_id)
    self._file_table.update(result.files)
```

**Why:**

- UI remains responsive during long operations
- Users see progress updates
- Application feels polished
- No frozen window complaints

---

## Principle 7: Every Feature Is Testable Without the GUI

**What it means:**

If a feature requires Qt or a running GUI to test, it's too tightly coupled to the UI.

**Example (❌ Avoid):**

```python
# Can't test without Qt
class FileDownloader:
    def download(self):
        self._ui.show_progress()  # ❌ Depends on UI
        await self._download_media()
        self._ui.show_completion()
```

**Example (✅ Prefer):**

```python
# Can test with simple callback
class DownloadManager:
    async def download(
        self,
        files: list[FileInfo],
        destination: Path,
        progress_callback: Callable[[DownloadProgress], None] | None = None,
    ) -> DownloadResult:
        # ✅ Progress is optional callback, not UI-specific
        ...
```

**Why:**

- Tests run faster (no GUI overhead)
- Tests are simpler to write
- Tests can run in CI without display
- Business logic is verifiable independent of UI

---

## Principle 8: Optimize Only After Measuring

**What it means:**

Never optimize based on assumptions. Measure first. If it's fast enough, leave it alone.

**Example (❌ Avoid):**

```python
# Premature optimization
class Scanner:
    def __init__(self):
        self._file_cache = {}
        self._lock = asyncio.Lock()
        # ❌ Added caching "just in case" it might be slow
```

**Example (✅ Prefer):**

```python
# Measure first
import timeit

async def scan_1000_files():
    start = timeit.default_timer()
    result = await scanner.scan_channel(123)
    elapsed = timeit.default_timer() - start
    print(f"Scanned 1000 files in {elapsed:.2f}s")
    # If <2s, we're done. If >2s, then optimize.
```

**Why:**

- Premature optimization adds complexity
- We're often wrong about bottlenecks
- Complexity has a real cost (maintenance, bugs)
- Measure before spending time optimizing

---

## Principle 9: Every Architectural Decision Should Reduce Future Complexity

**What it means:**

If an architectural choice makes the codebase harder to change later, it's the wrong choice.

**Example (❌ Avoid):**

```python
# Global singleton makes future features harder
class TelegramService:
    _instance = None
    
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = TelegramService()
        return cls._instance
    # ❌ Hard to test, hard to inject, hard to have multiple instances
```

**Example (✅ Prefer):**

```python
# Dependency injection makes future features easier
def main():
    telegram = TelegramService()
    scanner = TelegramScanner(telegram)
    downloader = DownloadManager(telegram)
    window = MainWindow(scanner, downloader)
    # ✅ Easy to test, easy to inject, easy to have multiple instances
```

**Why:**

- Architecture should enable, not hinder, future features
- Tight coupling makes refactoring painful
- Loose coupling (DI, composition) reduces friction
- Good architecture pays dividends over months/years

---

## Principle 10: If a Feature Requires Changing Multiple Layers, Define Interfaces First

**What it means:**

When adding a feature that spans layers (e.g., persistence), design the contracts (interfaces) before implementing.

**Example (❌ Avoid):**

```python
# Start coding without design
class Database:
    ...

# Halfway through, realize we need repositories
class ChannelRepository:
    ...

# But now we're tangled in SQLite details
# Refactoring is painful
```

**Example (✅ Prefer):**

```python
# Design interfaces first
class ChannelRepository(Protocol):
    async def save(self, channel: Channel) -> None: ...
    async def find(self, channel_id: int) -> Channel | None: ...

# Then implement against the interface
class SqliteChannelRepository(ChannelRepository):
    # Implementation follows from clear contract
    ...
```

**Why:**

- Interfaces clarify responsibilities before code exists
- Implementations can be reviewed against contracts
- Changes are localized (interface vs. implementation)
- Testing is simpler (mock the interface)

---

## Applying the Principles

When reviewing code or making decisions, ask:

1. **Composition?** Can this be built by combining simpler objects?
2. **Single responsibility?** Does this class have one reason to change?
3. **UI owns logic?** Is any business logic hiding in the UI?
4. **Infrastructure isolated?** Would changing SQLite to PostgreSQL be easy?
5. **Types explicit?** Are all contracts clearly defined?
6. **Non-blocking?** Is the UI responsive during long operations?
7. **Testable?** Can this be tested without Qt?
8. **Measured?** Did we verify this is actually slow before optimizing?
9. **Reduces complexity?** Will this make future changes easier or harder?
10. **Interfaces first?** Did we define contracts before implementation?

**If you answer "no" to any of these, reconsider the design.**

---

## Summary

These ten principles are not dogma. They're guardrails.

They exist to:

- Keep the codebase healthy
- Reduce the cost of future changes
- Make the project enjoyable to work on
- Enable the team to move fast without fear of breaking things

Follow them. When you encounter a situation where they conflict, explicitly document why you're making an exception. (
Exceptions are sometimes necessary; blindly following principles is also a mistake.)

Over time, these principles become instinct. You'll write code that naturally follows them without thinking about it.

That's when a codebase truly becomes a pleasure to work on.
