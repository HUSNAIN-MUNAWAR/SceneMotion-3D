from pathlib import Path
import cv2
from .extractors import FeatureExtractor


def visualize_keypoints(frame_path: str, output_path: str, method: str = "ORB") -> str:
    image = cv2.imread(frame_path)
    if image is None:
        raise ValueError(f"Could not read frame: {frame_path}")
    extractor = FeatureExtractor(method)
    kps, _ = extractor.detect_and_compute(image)
    vis = cv2.drawKeypoints(image, kps, None, flags=cv2.DrawMatchesFlags_DRAW_RICH_KEYPOINTS)
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(output_path, vis)
    return output_path
