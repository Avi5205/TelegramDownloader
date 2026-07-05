# ADR-003: Qt Model-View Pattern

## Status

Accepted

## Context

The file table in TGVault needed to support features like searching, filtering, sorting, and multi-selection. Qt
provides a Model-View architecture specifically designed for this use case, which separates data representation from
presentation.

## Decision

We use Qt's Model-View pattern:

- **FileTableModel** (QAbstractTableModel): Owns the data (list of FileInfo objects).
- **FileFilterProxyModel** (QSortFilterProxyModel): Wraps the model, providing search/filter/sort.
- **FileTableWidget** (QTableView): Presents the data, handles user interactions.

```
MainWindow (owns models and widget)
    │
    ├── FileTableModel
    │   └── [FileInfo, FileInfo, ...]
    │
    ├── FileFilterProxyModel (wraps model)
    │   └── Applies search, filter, sort
    │
    └── FileTableWidget (owns QTableView)
        └── Displays proxy model
```

## Consequences

### Positive

- **Separation of Concerns**: Data (model) is separate from presentation (view).
- **Filtering/Sorting**: Proxy model handles these efficiently without duplicating data.
- **Reusability**: Model can be used with different views (table, tree, list).
- **Performance**: Changes to one file don't require reloading the entire table.
- **Qt Native**: Uses Qt's optimized infrastructure; no reinventing the wheel.

### Negative

- **Complexity**: Requires understanding three classes instead of one.
- **Boilerplate**: Model classes require implementing abstract methods.

## Alternatives Considered

1. **Custom View Class**: Build a table from scratch. Rejected: reinvents the wheel, Qt's implementation is better.
2. **Simple QTableWidget**: Direct data binding. Rejected: doesn't support filtering/sorting elegantly.
3. **ListView with Custom Delegate**: Works but less natural for tabular data.

## Related ADRs

- ADR-001: Clean layered architecture
