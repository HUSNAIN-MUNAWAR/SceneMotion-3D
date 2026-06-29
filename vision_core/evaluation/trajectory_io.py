from __future__ import annotations
from pathlib import Path
import json
import numpy as np


def _as_float_tokens(line: str):
    if not line.strip() or line.lstrip().startswith('#'):
        return None
    try:
        return [float(x) for x in line.replace(',', ' ').split()]
    except ValueError:
        return None


def save_tum_trajectory(path: str | Path, timestamps, positions, quaternions=None) -> str:
    path = Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    positions = np.asarray(positions, dtype=float).reshape(-1, 3)
    timestamps = np.asarray(timestamps if timestamps is not None else np.arange(len(positions)), dtype=float)
    if quaternions is None:
        quaternions = np.tile(np.array([0.0, 0.0, 0.0, 1.0]), (len(positions), 1))
    lines = []
    for ts, p, q in zip(timestamps, positions, quaternions):
        lines.append(f"{ts:.6f} {p[0]:.9f} {p[1]:.9f} {p[2]:.9f} {q[0]:.9f} {q[1]:.9f} {q[2]:.9f} {q[3]:.9f}\n")
    path.write_text(''.join(lines), encoding='utf-8')
    return str(path)


def load_tum_trajectory(path: str | Path) -> dict:
    timestamps, positions, quats = [], [], []
    for line in Path(path).read_text(encoding='utf-8').splitlines():
        vals = _as_float_tokens(line)
        if vals is None or len(vals) < 8:
            continue
        timestamps.append(vals[0]); positions.append(vals[1:4]); quats.append(vals[4:8])
    return {"format": "tum", "timestamps": np.asarray(timestamps, dtype=float), "positions": np.asarray(positions, dtype=float), "quaternions": np.asarray(quats, dtype=float)}


def load_kitti_trajectory(path: str | Path) -> dict:
    poses, positions, timestamps = [], [], []
    for i, line in enumerate(Path(path).read_text(encoding='utf-8').splitlines()):
        vals = _as_float_tokens(line)
        if vals is None:
            continue
        if len(vals) == 12:
            M = np.asarray(vals, dtype=float).reshape(3, 4)
        elif len(vals) >= 13:
            M = np.asarray(vals[-12:], dtype=float).reshape(3, 4)
        else:
            continue
        poses.append(M); positions.append(M[:, 3]); timestamps.append(float(i))
    return {"format": "kitti", "timestamps": np.asarray(timestamps), "positions": np.asarray(positions), "poses": np.asarray(poses)}


def load_euroc_trajectory(path: str | Path) -> dict:
    timestamps, positions, quats = [], [], []
    for line in Path(path).read_text(encoding='utf-8').splitlines():
        if line.strip().startswith('#') or 'timestamp' in line.lower():
            continue
        vals = _as_float_tokens(line)
        if vals is None or len(vals) < 8:
            continue
        timestamps.append(vals[0]); positions.append(vals[1:4]); quats.append(vals[4:8])
    return {"format": "euroc", "timestamps": np.asarray(timestamps, dtype=float), "positions": np.asarray(positions, dtype=float), "quaternions": np.asarray(quats, dtype=float)}


def load_json_trajectory(path: str | Path) -> dict:
    data = json.loads(Path(path).read_text(encoding='utf-8'))
    poses = data.get('poses', data.get('trajectory', []))
    positions = []
    timestamps = []
    for i, pose in enumerate(poses):
        if isinstance(pose, dict):
            t = pose.get('t', pose.get('translation', pose.get('position', [0,0,0])))
            ts = pose.get('timestamp', i)
        else:
            t = pose[-3:] if len(pose) >= 3 else [0,0,0]
            ts = i
        positions.append(t[:3]); timestamps.append(float(ts))
    return {"format": "json", "timestamps": np.asarray(timestamps, dtype=float), "positions": np.asarray(positions, dtype=float)}


def load_trajectory(path: str | Path, fmt: str | None = None) -> dict:
    path = Path(path)
    fmt = (fmt or path.suffix.lower().lstrip('.')).lower()
    if fmt in {'json'}:
        return load_json_trajectory(path)
    if fmt in {'kitti'} or ('kitti' in path.name.lower()):
        return load_kitti_trajectory(path)
    if fmt in {'csv', 'euroc'} or ('euroc' in path.name.lower()):
        return load_euroc_trajectory(path)
    return load_tum_trajectory(path)


def align_by_timestamp(est: dict, gt: dict, max_delta: float | None = None) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    e_ts = np.asarray(est['timestamps'], dtype=float); g_ts = np.asarray(gt['timestamps'], dtype=float)
    e_pos = np.asarray(est['positions'], dtype=float); g_pos = np.asarray(gt['positions'], dtype=float)
    if len(e_ts) == 0 or len(g_ts) == 0:
        return np.empty((0,3)), np.empty((0,3)), np.empty((0,))
    pairs = []
    for i, ts in enumerate(e_ts):
        j = int(np.argmin(np.abs(g_ts - ts)))
        delta = abs(g_ts[j] - ts)
        if max_delta is None or delta <= max_delta:
            pairs.append((i, j, delta))
    if not pairs:
        n = min(len(e_pos), len(g_pos))
        return e_pos[:n], g_pos[:n], np.arange(n, dtype=float)
    return np.asarray([e_pos[i] for i,_,_ in pairs]), np.asarray([g_pos[j] for _,j,_ in pairs]), np.asarray([d for *_,d in pairs])
