from __future__ import annotations
import cv2
import numpy as np

class KeyframeDatabase:
    def __init__(self):
        self.records = []

    @staticmethod
    def descriptor_for_image(image_path: str) -> np.ndarray:
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            return np.zeros(64, dtype=float)
        orb = cv2.ORB_create(nfeatures=800)
        _, desc = orb.detectAndCompute(img, None)
        if desc is None or len(desc) == 0:
            return np.zeros(64, dtype=float)
        hist, _ = np.histogram(desc.ravel(), bins=64, range=(0, 256), density=True)
        return hist.astype(float)

    def add(self, frame_id: int, image_path: str):
        desc = self.descriptor_for_image(image_path)
        self.records.append({"frame_id": int(frame_id), "image_path": image_path, "descriptor": desc})

    def query(self, image_path: str, min_gap: int = 4, top_k: int = 5):
        q = self.descriptor_for_image(image_path)
        qn = np.linalg.norm(q) + 1e-12
        scored = []
        for r in self.records:
            score = float(np.dot(q, r['descriptor']) / (qn * (np.linalg.norm(r['descriptor']) + 1e-12)))
            scored.append({"frame_id": r['frame_id'], "image_path": r['image_path'], "score": score})
        scored.sort(key=lambda x: x['score'], reverse=True)
        return scored[:top_k]
