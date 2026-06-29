from pathlib import Path
import cv2
import numpy as np
from .depth_provider import DepthProvider

class FallbackDepthProvider(DepthProvider):
    name = "fallback_pseudo_depth"

    def __init__(self, reason: str = "Offline-safe pseudo-depth fallback; not metric depth."):
        self.reason = reason

    def estimate(self, image_path: str | Path) -> dict:
        return self.predict(image_path)

    def predict(self, image_path: str | Path) -> dict:
        img = cv2.imread(str(image_path))
        if img is None:
            raise ValueError(f"Could not read image: {image_path}")
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY).astype(np.float32) / 255.0
        blur = cv2.GaussianBlur(gray, (21, 21), 0)
        y_grad = np.linspace(0.3, 1.0, blur.shape[0], dtype=np.float32)[:, None]
        depth = 0.55 * (1.0 - blur) + 0.45 * y_grad
        depth = (depth - depth.min()) / max(float(depth.max() - depth.min()), 1e-6)
        depth = depth.astype(np.float32)
        return {"depth": depth, "confidence": float(np.std(depth)), "provider": self.name, "warning": self.reason}
