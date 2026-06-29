from typing import Literal, Optional, List, Dict, Any
from pydantic import BaseModel, Field

class JobStartRequest(BaseModel):
    source: Literal["sample", "uploaded"] = "sample"
    sample_name: Optional[str] = "synthetic_scene.mp4"
    upload_id: Optional[str] = None
    config: Dict[str, Any] = Field(default_factory=dict)

class JobStatus(BaseModel):
    job_id: str
    status: Literal["queued", "running", "completed", "failed"]
    progress: int
    stage: str
    message: str = ""
    warnings: List[str] = Field(default_factory=list)
    error: Optional[str] = None

class Artifact(BaseModel):
    name: str
    path: str
    type: str

class SampleVideo(BaseModel):
    name: str
    path: str
    size_bytes: int
