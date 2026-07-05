# Changelog

All notable changes to TGVault will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [0.1.0] - 2026-07-05

### Added

- Core user authentication with Telethon
- Channel discovery and listing
- File scanning within channels with category detection
- Search and filtering by name, category, and size range
- Multi-file selection with extended selection mode
- Download management with progress tracking
- Async UI with qasync and responsive event loop
- Clean layered architecture (Presentation → Application → Domain → Infrastructure)
- Dependency injection for all services
- Qt Model-View pattern for table rendering
- Comprehensive type hints throughout
- Unit tests for core components

### Architecture

- Established clean separation of concerns
- Single TelegramService instance shared across scanner and downloader
- Repository pattern for data access
- Domain models as pure dataclasses
- Async task management to prevent concurrent operations

### Repository Standards

- Issue templates (bug, feature, technical task)
- Architecture Decision Records (ADRs)
- API documentation

---

## [0.2.0] - Planned

### Planned Features

- SQLite persistence layer
- Channel and file metadata caching
- Download history and deduplication
- Scan result persistence across sessions
- Smart cache invalidation

---

## Notes

- **Versioning**: Uses Semantic Versioning (MAJOR.MINOR.PATCH)
- **Version Tags**: Each release will be tagged as `v0.x.x` in git
- **Breaking Changes**: Will be documented under `### Changed` with upgrade notes
