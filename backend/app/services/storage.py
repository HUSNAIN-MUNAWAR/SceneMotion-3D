from pathlib import Path
import uuid
from backend.app.core.config import get_settings
from backend.app.core.security import safe_child_path

class LocalStorage:
    def __init__(self):
        self.settings = get_settings()

    def new_job_dir(self, prefix: str = "job") -> tuple[str, Path]:
        job_id = f"{prefix}_{uuid.uuid4().hex[:12]}"
        out = safe_child_path(self.settings.output_dir, job_id)
        out.mkdir(parents=True, exist_ok=False)
        return job_id, out

    def uploads_dir(self) -> Path:
        p = safe_child_path(self.settings.output_dir, "uploads")
        p.mkdir(parents=True, exist_ok=True)
        return p
