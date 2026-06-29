import json
from pathlib import Path
import numpy as np
from .quality_checks import trajectory_length


def chain_poses(relative_poses: list[dict]) -> dict:
    R_global = np.eye(3, dtype=np.float64)
    t_global = np.zeros((3, 1), dtype=np.float64)
    poses = [{"index": 0, "R": R_global.tolist(), "t": t_global.ravel().tolist()}]
    for i, rp in enumerate(relative_poses, start=1):
        R = np.asarray(rp["R"], dtype=np.float64)
        t = np.asarray(rp["t"], dtype=np.float64).reshape(3, 1)
        # Relative monocular scale only; normalize step to unit direction when valid.
        norm = np.linalg.norm(t)
        if norm > 1e-9:
            t = t / norm
        t_global = t_global + R_global @ t
        R_global = R @ R_global
        poses.append({"index": i, "R": R_global.tolist(), "t": t_global.ravel().tolist(), "relative_scale": True})
    positions = [p["t"] for p in poses]
    return {"poses": poses, "positions": positions, "trajectory_length_relative": trajectory_length(positions), "scale_note": "Relative monocular units only."}


def save_trajectory(trajectory: dict, path: str | Path) -> str:
    Path(path).write_text(json.dumps(trajectory, indent=2), encoding="utf-8")
    return str(path)
