from pathlib import Path
import cv2
import numpy as np
import json

ROOT = Path(__file__).resolve().parents[1]
VIDEO_DIR = ROOT / "sample_data" / "videos"
VIDEO_DIR.mkdir(parents=True, exist_ok=True)


def main():
    out_path = VIDEO_DIR / "synthetic_scene.mp4"
    width, height = 640, 420
    fps = 12
    frames = 48
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    writer = cv2.VideoWriter(str(out_path), fourcc, fps, (width, height))
    rng = np.random.default_rng(42)
    base_points = rng.uniform([60, 60], [width - 60, height - 60], size=(80, 2))
    colors = rng.integers(50, 255, size=(80, 3)).tolist()
    for i in range(frames):
        img = np.zeros((height, width, 3), dtype=np.uint8)
        img[:] = (18, 22, 30)
        shift = np.array([i * 2.0, np.sin(i / 5) * 8.0])
        scale = 1.0 + i * 0.002
        center = np.array([width / 2, height / 2])
        for j, pt in enumerate(base_points):
            p = center + (pt - center) * scale + shift
            x, y = int(p[0]), int(p[1])
            if 0 <= x < width and 0 <= y < height:
                cv2.circle(img, (x, y), 3 + (j % 3), colors[j], -1)
                if j % 5 == 0:
                    cv2.rectangle(img, (x - 8, y - 8), (x + 8, y + 8), colors[j], 1)
        cv2.putText(img, f"SceneMotion synthetic frame {i:02d}", (24, 36), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (220, 220, 220), 2)
        writer.write(img)
    writer.release()
    calib = ROOT / "sample_data" / "sample_intrinsics.json"
    calib.write_text(json.dumps({"fx": 768.0, "fy": 768.0, "cx": width/2, "cy": height/2, "width": width, "height": height, "source": "synthetic_approx"}, indent=2), encoding="utf-8")
    print(out_path)

if __name__ == "__main__":
    main()
