import json
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from backend.app.services.job_store import job_store
from backend.app.core.security import safe_child_path
from vision_core.artifacts.bundle_exporter import create_artifact_bundle

router = APIRouter(prefix="/api/jobs", tags=["artifacts"])

def _job_or_404(job_id: str):
    job = job_store.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

@router.get("/{job_id}/artifacts")
def list_artifacts(job_id: str):
    job = _job_or_404(job_id)
    artifacts_path = job.output_dir / "artifacts.json"
    if artifacts_path.exists():
        return json.loads(artifacts_path.read_text())
    files = [str(p.relative_to(job.output_dir)) for p in job.output_dir.rglob("*") if p.is_file()]
    return {"job_id": job_id, "files": files}

@router.get("/{job_id}/frames")
def list_frames(job_id: str):
    job = _job_or_404(job_id)
    return sorted(str(p.relative_to(job.output_dir)) for p in (job.output_dir / "frames").glob("*.jpg"))

@router.get("/{job_id}/trajectory")
def get_trajectory(job_id: str):
    job = _job_or_404(job_id)
    path = job.output_dir / "trajectory.json"
    if not path.exists():
        raise HTTPException(status_code=404, detail="Trajectory not ready")
    return json.loads(path.read_text())

@router.get("/{job_id}/pointcloud")
def get_pointcloud(job_id: str, dense: bool = False):
    job = _job_or_404(job_id)
    name = "dense_cloud.ply" if dense else "sparse_cloud.ply"
    path = job.output_dir / "pointclouds" / name
    if not path.exists():
        raise HTTPException(status_code=404, detail="Point cloud not ready")
    return FileResponse(path, media_type="application/octet-stream", filename=name)

@router.get("/{job_id}/report")
def get_report(job_id: str, fmt: str = "html"):
    job = _job_or_404(job_id)
    name = "report.pdf" if fmt == "pdf" else "report.html"
    path = job.output_dir / name
    if not path.exists():
        raise HTTPException(status_code=404, detail="Report not ready")
    media = "application/pdf" if fmt == "pdf" else "text/html"
    return FileResponse(path, media_type=media, filename=name)


@router.get('/{job_id}/bundle')
def get_bundle(job_id: str):
    job = _job_or_404(job_id)
    bundle = create_artifact_bundle(job.output_dir, job.output_dir / 'artifact_bundle.zip')
    return FileResponse(bundle, media_type='application/zip', filename='artifact_bundle.zip')

@router.get("/{job_id}/artifact/{path:path}")
def get_artifact(job_id: str, path: str):
    job = _job_or_404(job_id)
    target = safe_child_path(job.output_dir, path)
    if not target.exists() or not target.is_file():
        raise HTTPException(status_code=404, detail="Artifact not found")
    return FileResponse(target)
