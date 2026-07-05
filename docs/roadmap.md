# TGVault Roadmap

## v0.1.0 ✅ Alpha — Complete

**Core scanning & downloading**

- [x] User authentication (Telethon session)
- [x] Channel discovery and listing
- [x] File scanning within channels
- [x] Search and filtering
- [x] Multi-file selection
- [x] Download orchestration
- [x] Progress reporting

**Architecture milestones:**

- [x] Clean layered architecture
- [x] Dependency injection
- [x] Qt Model-View pattern
- [x] Async UI with qasync
- [x] Separation of concerns

---

## v0.2.0 🎯 Persistence — In Planning

**SQLite integration for smart caching**

### Issues

- [ ] **DB-001**: Database connection layer (aiosqlite wrapper with UnitOfWork)
- [ ] **DB-002**: Migration engine (SQL migration system with tracking)
- [ ] **DB-003**: Migration tests (verify schema integrity)
- [ ] **DB-004**: ChannelRepository (cache channels)
- [ ] **DB-005**: FileRepository (cache file metadata)
- [ ] **DB-006**: DownloadRepository (track download history)
- [ ] **DB-007**: Persist scan results (wire TelegramScanner)
- [ ] **DB-008**: Load cached scans (offline mode on startup)
- [ ] **DB-009**: Persist download history (record all downloads)
- [ ] **DB-010**: Duplicate detection (skip already-downloaded files)
- [ ] **DB-011**: Repository tests (comprehensive coverage)

### Goals

- Reduce API load by caching scan results
- Skip rescanning channels that haven't changed (TTL: 7 days)
- Browse offline with cached data
- Prevent duplicate downloads
- Build foundation for queue, resume, favorites

### Key Technologies

- **aiosqlite**: Async SQLite wrapper
- **UnitOfWork**: Transaction boundary pattern
- **Protocols**: Define repository contracts before implementation
- **Migrations**: SQL-based version control for schema
- **aiosemaphore**: Serialize writes to SQLite

### Metrics

- Second scan of same channel: <100ms (cached)
- First scan of 1000-file channel: ~2s (network-bound)
- Offline browsing: instantly responsive
- Download deduplication: <1ms lookup

---

## v0.3.0 Download Engine

**Resume, retry, and queue**

- [ ] Resume interrupted downloads
- [ ] Automatic retry on failure
- [ ] Download queue (FIFO)
- [ ] Parallel downloads (configurable concurrency)
- [ ] Cancel/pause operations
- [ ] Download speed optimization

**Goals:**

- Handle large batches without UI freezing
- Recover gracefully from network interruptions
- Improve throughput for users with high bandwidth

---

## v0.4.0 Power User Features

**Productivity tools for power users**

- [ ] File preview (images, documents)
- [ ] Export file metadata (CSV, JSON)
- [ ] Bulk rename (regex patterns)
- [ ] Duplicate detection
- [ ] Smart filters (by date, size, type)
- [ ] Favorites and collections
- [ ] Recent downloads

**Goals:**

- Make TGVault indispensable for managing large Telegram archives

---

## v0.5.0 Performance & Polish

**Optimization and UX refinement**

- [ ] Download speed profiling
- [ ] Memory optimization for large scans
- [ ] UI responsiveness improvements
- [ ] Caching optimizations
- [ ] Keyboard shortcuts
- [ ] Drag-and-drop support
- [ ] Dark mode support

**Goals:**

- Sub-second UI response times
- Support scanning channels with 100k+ files

---

## v1.0.0 Production Release

**Enterprise-grade desktop application**

- [ ] Installer (Windows, macOS, Linux)
- [ ] Auto-update mechanism
- [ ] Comprehensive logging
- [ ] Settings/preferences UI
- [ ] User documentation
- [ ] API documentation
- [ ] CI/CD pipeline
- [ ] Code signing
- [ ] Packaged executable

**Goals:**

- Production-ready release
- Professional installer experience
- Ongoing updates without user intervention

---

## Post-1.0 Enhancements

### Cloud Sync (v1.1.0)

- Sync downloads across devices
- Cloud backup of metadata

### Advanced Search (v1.2.0)

- Full-text search in file names
- Saved searches
- Smart filters

### Team Features (v1.3.0)

- Multi-user authentication
- Team workspaces
- Shared scan results

### API & Extensibility (v1.4.0)

- REST API for downloads
- Plugin system
- Third-party integrations

---

## Quarterly Planning

### Q3 2026

- v0.2.0 Persistence (3 weeks)
- v0.3.0 Download Engine (2 weeks)
- v0.4.0 Power Features (1 week)

### Q4 2026

- v0.5.0 Performance (1 week)
- v1.0.0 Production Release (3 weeks)

### 2027+

- Cloud and advanced features

