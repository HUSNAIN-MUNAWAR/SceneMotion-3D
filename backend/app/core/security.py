from pathlib import Path

ALLOWED_VIDEO_SUFFIXES = {".mp4", ".mov", ".avi", ".mkv"}

def validate_video_path(path: Path) -> None:
    if path.suffix.lower() not in ALLOWED_VIDEO_SUFFIXES:
        raise ValueError(f"Unsupported video type: {path.suffix}")
    if not path.exists():
        raise FileNotFoundError(str(path))

def safe_child_path(base: Path, *parts: str) -> Path:
    base = base.resolve()
    target = base.joinpath(*parts).resolve()
    if base not in target.parents and target != base:
        raise ValueError("Unsafe path traversal attempt")
    return target
