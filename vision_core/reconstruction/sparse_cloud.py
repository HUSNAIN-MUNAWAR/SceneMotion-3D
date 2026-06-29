from pathlib import Path
import json
import numpy as np
from .triangulation import triangulate_pair
from .ply_exporter import export_ply


def build_sparse_cloud(match_dir: str | Path, pose_pairs: dict, K: np.ndarray, output_dir: str | Path, max_points: int = 50000) -> dict:
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    all_points = []
    for pose in pose_pairs.get("valid", []):
        i, j = pose["pair"]
        p = Path(match_dir) / f"pair_{i:04d}_{j:04d}.npz"
        if not p.exists():
            continue
        data = np.load(p)
        pts = triangulate_pair(data["kp1"], data["kp2"], data["matches"], K, np.asarray(pose["R"]), np.asarray(pose["t"]))
        if len(pts):
            all_points.append(pts)
    cloud = np.vstack(all_points) if all_points else np.empty((0, 3), dtype=float)
    if len(cloud) > max_points:
        idx = np.linspace(0, len(cloud) - 1, max_points).astype(int)
        cloud = cloud[idx]
    ply = export_ply(cloud, output_dir / "sparse_cloud.ply")
    json_path = output_dir / "sparse_cloud.json"
    json_path.write_text(json.dumps({"points": cloud[:5000].tolist(), "point_count": int(len(cloud)), "scale": "relative"}), encoding="utf-8")
    return {"point_count": int(len(cloud)), "ply": ply, "json": str(json_path)}
