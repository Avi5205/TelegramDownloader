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

## v0.2.0 🎯 Persistence

**SQLite integration for smart caching**

- [ ] Database connection layer
- [ ] Schema migrations (001_initial.sql)
- [ ] ChannelRepository (cache channels)
- [ ] FileRepository (cache file metadata)
- [ ] ScanCache (avoid rescanning unchanged channels)
- [ ] DownloadHistory (track downloaded files)
- [ ] Persistence tests

**Goals:**

- Reduce API load by caching scan results
- Skip rescanning channels that haven't changed
- Build foundation for future features

**Metrics:**

- Second scan of same channel takes <100ms
- Download history prevents duplicate downloads

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

- v0.2.0 Persistence (2 weeks)
- v0.3.0 Download Engine (2 weeks)
- v0.4.0 Power Features (2 weeks)

### Q4 2026

- v0.5.0 Performance (1 week)
- v1.0.0 Production Release (3 weeks)

### 2027+

- Cloud and advanced features
