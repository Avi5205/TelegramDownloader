# Definition of Done (DoD)

Every completed issue must satisfy its specific DoD before merge.

---

## General DoD (All Issues)

- [ ] Code follows project style guidelines
- [ ] All tests pass (unit, integration, migration)
- [ ] No new warnings or linting errors
- [ ] Commit message follows Conventional Commits
- [ ] PR description is clear and links to issue
- [ ] Self-review completed before requesting review
- [ ] No hardcoded credentials or secrets
- [ ] Architecture rules followed (clean layering, no UI-to-DB coupling)

---

## DB-001: Database Connection Layer

**Objective:** Create async SQLite wrapper with transaction support.

- [ ] `Database` class created in `src/database/connection.py`
- [ ] Uses `aiosqlite` for async operations
- [ ] Supports async context manager (`async with Database(...) as db`)
- [ ] `execute()` method for read queries (async)
- [ ] `execute_write()` method for write queries with lock (async)
- [ ] Write lock prevents concurrent writes to SQLite
- [ ] Connection pool strategy documented (initially: single connection)
- [ ] Logging added (INFO: connect/disconnect, DEBUG: queries)
- [ ] Unit tests for all public methods
- [ ] No UI or Qt dependencies
- [ ] No SQL outside repository layer (future enforcement)
- [ ] Error handling for disk full, corrupted DB, file permissions
- [ ] Ready for PR review

---

## DB-002: Migration Engine

**Objective:** Implement SQL migration system with tracking.

- [ ] `Migration` dataclass defined (number, name, up_sql, down_sql)
- [ ] `Migrator` class created in `src/database/migrations.py`
- [ ] Migrations directory: `src/database/migrations/`
- [ ] `_migrations` tracking table created automatically
- [ ] `migrate()` method applies pending migrations in order
- [ ] `rollback(steps)` method reverts N migrations
- [ ] Migration checksum prevents re-running (SHA256 of SQL)
- [ ] Applied migrations logged (version, timestamp, checksum)
- [ ] Tests verify forward + rollback consistency
- [ ] First migration: `001_initial_schema.sql` (creates all tables)
- [ ] Error handling for invalid migrations, missing files, checksum mismatch
- [ ] Ready for PR review

---

## DB-003: Migration Tests

**Objective:** Verify migrations apply cleanly and can be rolled back.

- [ ] Test: Fresh database → all migrations apply successfully
- [ ] Test: Schema matches expected structure after migration
- [ ] Test: Each migration can be rolled back without error
- [ ] Test: Rollback + re-apply produces identical schema
- [ ] Test: Forward migration order matters (E2E)
- [ ] Test: Missing migration file raises error
- [ ] Test: Corrupted migration SQL raises error
- [ ] Test: Checksum mismatch prevents re-running
- [ ] All tests pass with coverage >95%
- [ ] Ready for PR review

---

## DB-004: ChannelRepository

**Objective:** Implement ChannelRepository with full CRUD and caching.

- [ ] `ChannelRepository` class defined as `Protocol` first
- [ ] `ChannelRepository` implementation in `src/database/repositories/channel_repository.py`
- [ ] Depends on `UnitOfWork` (not raw `Database`)
- [ ] `async save(channel: Channel)` → INSERT or UPDATE
- [ ] `async find(channel_id: int)` → single channel or None
- [ ] `async list()` → all cached channels
- [ ] `async delete(channel_id: int)` → delete channel and cascade files/downloads
- [ ] `async set_scan_status(channel_id: int, status: str)` → pending/scanning/complete/failed
- [ ] `async get_scan_status(channel_id: int)` → current status
- [ ] Unit tests for all methods (mocked UnitOfWork)
- [ ] Integration tests with real database
- [ ] Index on `username` for searches
- [ ] Index on `last_scanned_at` for cache invalidation queries
- [ ] No SQL leaks to UI layer
- [ ] Ready for PR review

---

## DB-005: FileRepository

**Objective:** Implement FileRepository with search and filtering.

- [ ] `FileRepository` class defined as `Protocol` first
- [ ] `FileRepository` implementation in `src/database/repositories/file_repository.py`
- [ ] Depends on `UnitOfWork` (not raw `Database`)
- [ ] `async save_files(channel_id: int, files: list[FileInfo])` → batch upsert
- [ ] `async find(file_id: str)` → single file or None
- [ ] `async find_by_channel(channel_id: int)` → all files in channel
- [ ] `async search(channel_id, query, category, min_size, max_size)` → filtered query
- [ ] `async delete_channel_files(channel_id: int)` → cascade delete
- [ ] Unit tests for all methods (mocked UnitOfWork)
- [ ] Integration tests with real database
- [ ] Indexes on: `channel_id`, `category`, `size`, `name`
- [ ] Search query performance <100ms on 10k files
- [ ] No SQL leaks to UI layer
- [ ] Ready for PR review

---

## DB-006: DownloadRepository

**Objective:** Implement DownloadRepository for download tracking.

- [ ] `DownloadRepository` class defined as `Protocol` first
- [ ] `DownloadRepository` implementation in `src/database/repositories/download_repository.py`
- [ ] Depends on `UnitOfWork` (not raw `Database`)
- [ ] `async record(file_id, channel_id, file_name, file_size, local_path, status)` → INSERT
- [ ] `async get_status(file_id: str)` → status or None
- [ ] `async list_history(channel_id, limit)` → recent downloads
- [ ] `async mark_failed(file_id: str, error: str)` → UPDATE status
- [ ] `async list_failed()` → all failed downloads (for retry feature)
- [ ] `async delete(file_id: str)` → remove download record
- [ ] Unit tests for all methods (mocked UnitOfWork)
- [ ] Integration tests with real database
- [ ] Indexes on: `status`, `file_id`, `channel_id`, `downloaded_at`
- [ ] Deduplication query performance <1ms
- [ ] No SQL leaks to UI layer
- [ ] Ready for PR review

---

## DB-007: Persist Scan Results

**Objective:** Wire TelegramScanner to save results to database.

- [ ] `TelegramScanner` accepts `ChannelRepository` and `FileRepository` in __init__
- [ ] After scan completes, save results: `await channel_repo.save(channel)`
- [ ] Save files: `await file_repo.save_files(channel_id, files)`
- [ ] Update scan status: `await channel_repo.set_scan_status(channel_id, 'complete')`
- [ ] Handle failures gracefully: `await channel_repo.set_scan_status(channel_id, 'failed')`
- [ ] Unit tests for scanner with mocked repositories
- [ ] Integration tests scanning real (mocked) channel
- [ ] Verify database contains expected records after scan
- [ ] Scan status transitions work correctly
- [ ] No UI changes (pure service layer)
- [ ] Ready for PR review

---

## DB-008: Load Cached Scans

**Objective:** Load channel list and files from database on startup.

- [ ] `MainWindow.__init__` calls `load_channels_from_cache()` 
- [ ] `load_channels_from_cache()` loads from database (not API)
- [ ] FileTableModel populated from cached files immediately
- [ ] TTL-based cache validation: rescan if `last_scanned_at < now() - 7 days`
- [ ] Stale channels queued for background rescan
- [ ] Startup time improves: ~instant vs. API call latency
- [ ] Unit tests for cache loading
- [ ] Integration tests with populated database
- [ ] Verify UI shows cached files before background rescan
- [ ] No API calls during initial load (offline mode works)
- [ ] Ready for PR review

---

## DB-009: Persist Download History

**Objective:** Record all downloads to database for history/deduplication.

- [ ] `DownloadManager` calls `download_repo.record()` before download
- [ ] After successful download: record `status='completed'`, `local_path=...`
- [ ] After failed download: record `status='failed'`, `error=...`
- [ ] Update `attempts` count on retry
- [ ] Unit tests for DownloadManager with mocked repository
- [ ] Integration tests with real database
- [ ] Download history appears in UI (future feature)
- [ ] Verify records created for each download attempt
- [ ] No UI changes (pure service layer)
- [ ] Ready for PR review

---

## DB-010: Duplicate Download Detection

**Objective:** Prevent re-downloading files that are already downloaded.

- [ ] Before downloading, check: `status = await download_repo.get_status(file_id)`
- [ ] If `status == 'completed'`, skip download and mark progress
- [ ] Show user feedback: "Already downloaded" instead of re-downloading
- [ ] Unit tests for duplication logic
- [ ] Integration tests verifying skipped downloads
- [ ] DownloadManager returns same result (bytes=0, skipped=true)
- [ ] Progress callbacks handle skipped files
- [ ] No UI changes (service layer only)
- [ ] Ready for PR review

---

## DB-011: Repository Tests

**Objective:** Comprehensive test coverage for all repositories.

- [ ] Unit test file: `tests/database/test_repositories.py`
- [ ] Each repository has >90% test coverage
- [ ] Tests cover: CRUD, edge cases, constraints, cascades
- [ ] Integration tests with real database
- [ ] Tests verify indexes are used (EXPLAIN QUERY PLAN)
- [ ] Performance benchmarks recorded (baseline for optimization)
- [ ] All tests pass: `pytest tests/database/`
- [ ] CI pipeline green
- [ ] Ready for PR review

---

## Acceptance Criteria Verification

Before moving to next issue, verify:

```
Does this issue:
- [ ] Satisfy its specific DoD?
- [ ] Pass general DoD?
- [ ] Maintain architecture?
- [ ] Add no > 500 lines?
- [ ] Include tests?
- [ ] Improve code quality?
```

If **all boxes are checked**, the issue is ready to merge.
