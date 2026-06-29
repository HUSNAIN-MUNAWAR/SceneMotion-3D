import json
from pathlib import Path
from .intrinsics import CameraIntrinsics, estimate_intrinsics


def load_intrinsics_json(path: str | Path) -> CameraIntrinsics:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    required = ["fx", "fy", "cx", "cy", "width", "height"]
    missing = [k for k in required if k not in data]
    if missing:
        raise ValueError(f"Missing intrinsics keys: {missing}")
    return CameraIntrinsics(**{k: data[k] for k in required}, source=data.get("source", "provided"))


def intrinsics_from_config(config: dict, width: int, height: int) -> CameraIntrinsics:
    if config.get("calibration_json"):
        return load_intrinsics_json(config["calibration_json"])
    if all(k in config for k in ["fx", "fy", "cx", "cy"]):
        return CameraIntrinsics(config["fx"], config["fy"], config["cx"], config["cy"], width, height, source="manual")
    return estimate_intrinsics(width, height, float(config.get("focal_factor", 1.2)))
