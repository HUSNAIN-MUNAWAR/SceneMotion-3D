from __future__ import annotations
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Any
import threading

@dataclass
class JobRecord:
    job_id: str
    video_path: Path
    output_dir: Path
    status: str = "queued"
    progress: int = 0
    stage: str = "queued"
    message: str = ""
    warnings: List[str] = field(default_factory=list)
    error: Optional[str] = None
    metrics: Optional[Dict[str, Any]] = None

class JobStore:
    def __init__(self):
        self._jobs: Dict[str, JobRecord] = {}
        self._lock = threading.Lock()

    def add(self, job: JobRecord) -> None:
        with self._lock:
            self._jobs[job.job_id] = job

    def get(self, job_id: str) -> Optional[JobRecord]:
        with self._lock:
            return self._jobs.get(job_id)

    def update(self, job_id: str, **kwargs) -> None:
        with self._lock:
            job = self._jobs[job_id]
            for k, v in kwargs.items():
                setattr(job, k, v)

    def list(self):
        with self._lock:
            return list(self._jobs.values())

    def remove(self, job_id: str):
        with self._lock:
            return self._jobs.pop(job_id, None)

job_store = JobStore()
