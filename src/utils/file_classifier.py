VIDEO_EXTENSIONS = {
    ".mp4",
    ".mkv",
    ".avi",
    ".mov",
    ".webm",
    ".flv",
}

IMAGE_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".gif",
    ".bmp",
    ".webp",
}

DOCUMENT_EXTENSIONS = {
    ".pdf",
    ".doc",
    ".docx",
    ".ppt",
    ".pptx",
    ".xls",
    ".xlsx",
    ".txt",
    ".epub",
}

AUDIO_EXTENSIONS = {
    ".mp3",
    ".wav",
    ".aac",
    ".flac",
    ".ogg",
}

ARCHIVE_EXTENSIONS = {
    ".zip",
    ".rar",
    ".7z",
    ".tar",
    ".gz",
}


def classify(filename: str | None) -> str:

    if not filename:
        return "others"

    filename = filename.lower()

    for extension in VIDEO_EXTENSIONS:
        if filename.endswith(extension):
            return "videos"

    for extension in IMAGE_EXTENSIONS:
        if filename.endswith(extension):
            return "images"

    for extension in DOCUMENT_EXTENSIONS:
        if filename.endswith(extension):
            return "documents"

    for extension in AUDIO_EXTENSIONS:
        if filename.endswith(extension):
            return "audio"

    for extension in ARCHIVE_EXTENSIONS:
        if filename.endswith(extension):
            return "archives"

    return "others"