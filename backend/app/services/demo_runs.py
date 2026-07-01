from __future__ import annotations

import json
from pathlib import Path

from backend.app.core.config import get_settings
from backend.app.services.job_store import JobRecord, job_store


def _load_metrics(path: Path) -> dict:
    try:
        return json.loads(path.read_text())
    except Exception:
        return {}


def hydrate_completed_runs() -> None:
    settings = get_settings()

    for output_dir in sorted(settings.output_dir.iterdir()):
        if not output_dir.is_dir():
            continue

        metrics_path = output_dir / "metrics.json"
        if not metrics_path.exists() or job_store.get(output_dir.name):
            continue

        metrics = _load_metrics(metrics_path)
        source_name = Path(str(metrics.get("video_path", "synthetic_scene.mp4"))).name
        video_path = settings.sample_dir / source_name
        if not video_path.exists():
            video_path = output_dir

        job_store.add(
            JobRecord(
                job_id=output_dir.name,
                video_path=video_path,
                output_dir=output_dir,
                status="completed",
                progress=100,
                stage="completed",
                message="Loaded from existing artifacts on disk.",
                warnings=list(metrics.get("warnings", [])),
                metrics=metrics,
            )
        )
