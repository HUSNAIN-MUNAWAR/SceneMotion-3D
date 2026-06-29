from pathlib import Path
import cv2
from .video_reader import read_video_metadata

def extract_frames(video_path: str | Path, output_dir: str | Path, target_fps: float = 3.0, max_frames: int = 240, resize_width: int | None = 960) -> dict:
    video_path = Path(video_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    meta = read_video_metadata(video_path)
    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        raise ValueError(f"Could not open video: {video_path}")
    src_fps = meta.fps if meta.fps > 0 else 30.0
    step = max(1, int(round(src_fps / max(target_fps, 0.1))))
    saved = []
    idx = 0
    out_idx = 0
    while len(saved) < max_frames:
        ok, frame = cap.read()
        if not ok:
            break
        if idx % step == 0:
            if resize_width and frame.shape[1] > resize_width:
                scale = resize_width / frame.shape[1]
                frame = cv2.resize(frame, (resize_width, int(frame.shape[0] * scale)), interpolation=cv2.INTER_AREA)
            path = output_dir / f"frame_{out_idx:05d}.jpg"
            cv2.imwrite(str(path), frame)
            saved.append(str(path))
            out_idx += 1
        idx += 1
    cap.release()
    result = meta.to_dict()
    result["selected_frame_count"] = len(saved)
    result["frame_paths"] = saved
    return result
