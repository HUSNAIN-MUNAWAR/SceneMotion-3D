from pathlib import Path
import json
import cv2
import numpy as np

class FeatureExtractor:
    def __init__(self, method: str = "ORB", max_features: int = 2000):
        self.method = method.upper()
        self.max_features = max_features
        self.extractor = self._create()

    def _create(self):
        if self.method == "SIFT" and hasattr(cv2, "SIFT_create"):
            return cv2.SIFT_create(nfeatures=self.max_features)
        if self.method == "AKAZE" and hasattr(cv2, "AKAZE_create"):
            return cv2.AKAZE_create()
        self.method = "ORB"
        return cv2.ORB_create(nfeatures=self.max_features, fastThreshold=7)

    def detect_and_compute(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if image.ndim == 3 else image
        kps, desc = self.extractor.detectAndCompute(gray, None)
        return kps or [], desc

    def descriptor_norm(self):
        return cv2.NORM_HAMMING if self.method in {"ORB", "AKAZE"} else cv2.NORM_L2


def keypoints_to_array(kps):
    if not kps:
        return np.empty((0, 2), dtype=np.float32)
    return np.array([kp.pt for kp in kps], dtype=np.float32)


def extract_features_for_keyframes(keyframe_paths: list[str], output_dir: str | Path, method: str = "ORB", max_features: int = 2000) -> dict:
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    extractor = FeatureExtractor(method, max_features)
    features = []
    counts = []
    for idx, fp in enumerate(keyframe_paths):
        img = cv2.imread(fp)
        if img is None:
            continue
        kps, desc = extractor.detect_and_compute(img)
        pts = keypoints_to_array(kps)
        desc_arr = desc if desc is not None else np.empty((0, 32), dtype=np.uint8)
        npz = output_dir / f"features_{idx:04d}.npz"
        np.savez_compressed(npz, keypoints=pts, descriptors=desc_arr, method=extractor.method)
        features.append({"frame": fp, "npz": str(npz), "keypoint_count": int(len(kps))})
        counts.append(int(len(kps)))
    payload = {"method": extractor.method, "features": features, "counts": counts, "average_keypoints": float(np.mean(counts)) if counts else 0.0}
    (output_dir / "feature_counts.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return payload
