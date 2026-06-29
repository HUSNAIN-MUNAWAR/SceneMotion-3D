from pathlib import Path
from dataclasses import dataclass, asdict
import cv2

@dataclass
class VideoMetadata:
    path: str
    duration: float
    fps: float
    frame_count: int
    width: int
    height: int

    def to_dict(self):
        return asdict(self)

def read_video_metadata(video_path: str | Path) -> VideoMetadata:
    video_path = Path(video_path)
    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        raise ValueError(f"Could not open video: {video_path}")
    fps = float(cap.get(cv2.CAP_PROP_FPS) or 0.0)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) or 0)
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) or 0)
    duration = frame_count / fps if fps > 0 else 0.0
    cap.release()
    return VideoMetadata(str(video_path), duration, fps, frame_count, width, height)
