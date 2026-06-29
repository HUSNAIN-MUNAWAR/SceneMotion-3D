from pathlib import Path
from threading import Thread
from backend.app.services.job_store import job_store, JobRecord
from backend.app.services.storage import LocalStorage
from backend.app.core.config import get_settings
from backend.app.core.security import validate_video_path, safe_child_path
from workers.pipeline_worker import run_pipeline_job

storage = LocalStorage()

def create_job_for_video(video_path: Path, config: dict | None = None) -> JobRecord:
    validate_video_path(video_path)
    job_id, out = storage.new_job_dir("job")
    job = JobRecord(job_id=job_id, video_path=video_path, output_dir=out)
    job_store.add(job)
    if (config or {}).get("dry_run"):
        job_store.update(job_id, status="queued", stage="dry_run", message="Dry-run job created without starting worker thread.")
        return job

    def progress_cb(progress: int, stage: str, message: str = "") -> None:
        job_store.update(job_id, progress=progress, stage=stage, message=message, status="running")

    def target():
        try:
            job_store.update(job_id, status="running", stage="starting", progress=1)
            metrics = run_pipeline_job(video_path, out, config or {}, progress_cb=progress_cb)
            job_store.update(job_id, status="completed", progress=100, stage="completed", metrics=metrics, warnings=metrics.get("warnings", []))
        except Exception as exc:  # defensive API boundary
            job_store.update(job_id, status="failed", error=str(exc), stage="failed", message=str(exc))

    Thread(target=target, daemon=True).start()
    return job

def get_sample_path(sample_name: str) -> Path:
    settings = get_settings()
    path = safe_child_path(settings.sample_dir, sample_name)
    validate_video_path(path)
    return path
