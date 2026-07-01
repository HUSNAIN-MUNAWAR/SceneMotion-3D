import asyncio
import json
from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect
from backend.app.schemas.jobs import JobStartRequest, JobStatus
from backend.app.services.job_service import create_job_for_video, get_sample_path
from backend.app.services.job_store import job_store
from backend.app.services.storage import LocalStorage
storage = LocalStorage()
from backend.app.core.security import safe_child_path

router = APIRouter(prefix="/api/jobs", tags=["jobs"])

@router.post("/start", response_model=JobStatus)
def start_job(req: JobStartRequest):
    if req.source == "sample":
        video_path = get_sample_path(req.sample_name or "synthetic_scene.mp4")
    elif req.source == "uploaded" and req.upload_id:
        video_path = safe_child_path(storage.uploads_dir(), req.upload_id)
    else:
        raise HTTPException(status_code=400, detail="Provide a sample_name or upload_id")
    job = create_job_for_video(video_path, req.config)
    return JobStatus(job_id=job.job_id, status=job.status, progress=job.progress, stage=job.stage)

@router.get("/{job_id}", response_model=JobStatus)
def get_job(job_id: str):
    job = job_store.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return JobStatus(job_id=job.job_id, status=job.status, progress=job.progress, stage=job.stage, message=job.message, warnings=job.warnings, error=job.error)

@router.get("/{job_id}/metrics")
def get_metrics(job_id: str):
    job = job_store.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    if job.metrics:
        return job.metrics
    metrics_path = job.output_dir / "metrics.json"
    if metrics_path.exists():
        return json.loads(metrics_path.read_text())
    raise HTTPException(status_code=404, detail="Metrics not ready")

@router.websocket("/{job_id}/stream")
async def stream_job(websocket: WebSocket, job_id: str):
    await websocket.accept()
    try:
        while True:
            job = job_store.get(job_id)
            if not job:
                await websocket.send_json({"error": "Job not found"})
                return
            await websocket.send_json({
                "job_id": job.job_id,
                "status": job.status,
                "progress": job.progress,
                "stage": job.stage,
                "message": job.message,
                "warnings": job.warnings,
                "error": job.error,
            })
            if job.status in {"completed", "failed"}:
                return
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        return


@router.post("/{job_id}/cancel")
def cancel_job(job_id: str):
    job = job_store.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    if job.status in {"completed", "failed"}:
        return {"job_id": job_id, "status": job.status, "message": "Job already finished"}
    job_store.update(job_id, status="cancelled", stage="cancelled", message="Cancellation requested. Local thread may finish current stage.")
    return {"job_id": job_id, "status": "cancelled"}

@router.delete("/{job_id}")
def delete_job(job_id: str):
    job = job_store.remove(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return {"job_id": job_id, "deleted": True, "note": "In-memory job record removed. Artifacts are kept unless cleaned manually."}
