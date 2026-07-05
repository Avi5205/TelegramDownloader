# ADR-001: Clean Layered Architecture

## Status

Accepted

## Context

TGVault needed a structure that could scale from a simple Telethon wrapper to a full desktop application without major refactoring. The application needed clear separation between user interface, business logic, and external service integration.

## Decision

We adopted a clean layered architecture with four distinct layers:

```
Presentation Layer
    ├── MainWindow
    ├── Widgets (FileTableWidget, ChannelDetailsWidget)
    └── Models (FileTableModel, FileFilterProxyModel)
         ↓
Application Layer
    ├── TelegramScanner
    ├── DownloadManager
    └── Repositories
         ↓
Domain Layer
    ├── Channel
    ├── FileInfo
    ├── ScanResult
    └── DownloadResult
         ↓
Infrastructure Layer
    └── TelegramService → Telethon
```

## Consequences

### Positive

- **Testability**: Each layer can be tested independently with mocks.
- **Maintainability**: Changes in one layer don't cascade to others.
- **Extensibility**: New features can be added without redesigning existing code.
- **Reusability**: Application services can be used in different UI contexts (CLI, web, etc.).
- **Dependency Direction**: Dependencies always flow inward (UI → Domain).

### Negative

- **Verbosity**: More files and classes than a monolithic approach.
- **Learning Curve**: New contributors must understand the layered structure.

## Alternatives Considered

1. **Monolithic**: Everything in one class. Rejected: would become unmaintainable at scale.
2. **MVC**: Model-View-Controller. Rejected: Qt's Model-View is superior for desktop apps.
3. **Hexagonal**: Ports and adapters. Accepted in principle; clean architecture is a superset.

## Related ADRs

- ADR-002: Single TelegramService instance
- ADR-003: Qt Model-View pattern
