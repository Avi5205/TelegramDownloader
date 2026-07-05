# ADR-002: Single TelegramService Instance

## Status

Accepted

## Context

The Telethon client is stateful and manages the Telegram connection, session, and entity cache. The application needed a way to share this single connection across multiple features (scanning, downloading, repository queries) without creating multiple instances or exposing Telethon directly.

## Decision

We created a single `TelegramService` instance that wraps the Telethon client. All other components depend on this single instance via dependency injection.

```
main.py
    │
    ├── telegram = TelegramService()  ← Single instance
    │
    ├── TelegramRepository(telegram)
    ├── TelegramScanner(telegram)
    ├── DownloadManager(telegram)
    │
    └── MainWindow(scanner, download_manager)
```

## Consequences

### Positive

- **Connection Management**: One authenticated session for the entire application.
- **Entity Cache**: Telethon's internal entity cache is shared, reducing redundant RPCs.
- **Testability**: Easy to mock for unit tests.
- **Composition**: Clear composition root in `main.py`.
- **Encapsulation**: Internal Telethon details are hidden behind `TelegramService`.

### Negative

- **Global State**: The service carries connection state.
- **Shutdown**: Requires explicit cleanup (handled in `main.py` with context manager).

## Alternatives Considered

1. **Multiple Instances**: Create a new client per operation. Rejected: wasteful, loses entity cache, harder to manage connections.
2. **Global Singleton**: Use `TelegramService.instance()`. Rejected: less testable, harder to inject mocks.
3. **Dependency on Telethon**: Pass Telethon client directly. Rejected: couples business logic to Telethon API.

## Related ADRs

- ADR-001: Clean layered architecture
- ADR-004: Repository pattern for data access
