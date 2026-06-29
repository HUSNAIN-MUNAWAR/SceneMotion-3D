from pathlib import Path
import json
import cv2
import numpy as np
from .depth_provider import get_depth_provider


def colorize_depth(depth: np.ndarray):
    arr = (255 * (depth - depth.min()) / max(float(depth.max() - depth.min()), 1e-6)).astype("uint8")
    return cv2.applyColorMap(arr, cv2.COLORMAP_TURBO)


def generate_depth_maps(keyframe_paths: list[str], output_dir: str | Path, provider_name: str = "fallback", max_maps: int = 6) -> dict:
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    provider = get_depth_provider(provider_name)
    maps = []
    warnings = []
    for i, frame in enumerate(keyframe_paths[:max_maps]):
        pred = provider.predict(frame)
        depth = pred["depth"]
        npy = output_dir / f"depth_{i:04d}.npy"
        png = output_dir / f"depth_{i:04d}.png"
        np.save(npy, depth)
        cv2.imwrite(str(png), colorize_depth(depth))
        if pred.get("warning"):
            warnings.append(pred["warning"])
        maps.append({"frame": frame, "npy": str(npy), "png": str(png), "provider": pred.get("provider", provider.name), "confidence": pred.get("confidence", 0.0)})
    payload = {"maps": maps, "count": len(maps), "provider": provider.name, "warnings": sorted(set(warnings))}
    (output_dir / "depth_metadata.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return payload
