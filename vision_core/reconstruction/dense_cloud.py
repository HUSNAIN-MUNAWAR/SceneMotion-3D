from pathlib import Path
import numpy as np
import cv2
from vision_core.reconstruction.ply_exporter import export_ply


def depth_to_points(depth: np.ndarray, image: np.ndarray | None, K: np.ndarray, stride: int = 4, max_depth: float = 1.0):
    h, w = depth.shape[:2]
    ys, xs = np.mgrid[0:h:stride, 0:w:stride]
    z = depth[ys, xs].astype(np.float32)
    valid = np.isfinite(z) & (z > 1e-6)
    fx, fy, cx, cy = K[0,0], K[1,1], K[0,2], K[1,2]
    X = (xs - cx) * z / fx
    Y = (ys - cy) * z / fy
    pts = np.stack([X, Y, z], axis=-1)[valid]
    colors = None
    if image is not None:
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        colors = rgb[ys, xs][valid]
    return pts, colors


def export_dense_cloud(depth_path: str | Path, image_path: str | Path, K: np.ndarray, output_path: str | Path, stride: int = 5) -> dict:
    depth = np.load(depth_path)
    image = cv2.imread(str(image_path))
    pts, colors = depth_to_points(depth, image, K, stride=stride)
    ply = export_ply(pts, output_path, colors)
    return {"point_count": int(len(pts)), "ply": ply}
