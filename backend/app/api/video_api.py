from pathlib import Path
from fastapi import APIRouter, UploadFile, File, HTTPException
from backend.app.core.config import get_settings
from backend.app.core.security import ALLOWED_VIDEO_SUFFIXES, safe_child_path
from backend.app.schemas.jobs import SampleVideo
from backend.app.services.storage import LocalStorage

router = APIRouter(prefix="/api/videos", tags=["videos"])
storage = LocalStorage()

@router.get("/samples", response_model=list[SampleVideo])
def list_samples():
    settings = get_settings()
    settings.sample_dir.mkdir(parents=True, exist_ok=True)
    samples = []
    for p in sorted(settings.sample_dir.glob("*")):
        if p.suffix.lower() in ALLOWED_VIDEO_SUFFIXES:
            samples.append(SampleVideo(name=p.name, path=str(p), size_bytes=p.stat().st_size))
    return samples

@router.post("/upload")
async def upload_video(file: UploadFile = File(...)):
    suffix = Path(file.filename or "video.mp4").suffix.lower()
    if suffix not in ALLOWED_VIDEO_SUFFIXES:
        raise HTTPException(status_code=400, detail="Unsupported video file type")
    settings = get_settings()
    max_bytes = settings.max_upload_mb * 1024 * 1024
    upload_id = Path(file.filename or "uploaded.mp4").stem.replace("/", "_").replace("\\", "_") + suffix
    target = safe_child_path(storage.uploads_dir(), upload_id)
    size = 0
    with target.open("wb") as f:
        while chunk := await file.read(1024 * 1024):
            size += len(chunk)
            if size > max_bytes:
                target.unlink(missing_ok=True)
                raise HTTPException(status_code=413, detail="Upload too large")
            f.write(chunk)
    return {"upload_id": target.name, "path": str(target), "size_bytes": size}
