from typing import Final

CATEGORY_LABELS: Final[dict[str, str]] = {
    "videos": "Video",
    "documents": "Document",
    "images": "Image",
    "audio": "Audio",
    "archives": "Archive",
    "others": "Other",
}

# Order in which categories should appear in UI combo boxes (optional)
CATEGORY_ORDER: Final[tuple[str, ...]] = (
    "videos",
    "documents",
    "images",
    "audio",
    "archives",
    "others",
)
