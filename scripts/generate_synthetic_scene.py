from pathlib import Path
import json
import numpy as np

ROOT = Path(__file__).resolve().parents[1]

def main():
    rng = np.random.default_rng(7)
    points = rng.uniform([-2, -1, 3], [2, 1, 8], size=(200, 3))
    poses = []
    for i in range(10):
        poses.append({"index": i, "t": [i * 0.1, 0, 0], "R": np.eye(3).tolist()})
    out = ROOT / "sample_data" / "synthetic_scene_points.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({"points": points.tolist(), "poses": poses}, indent=2), encoding="utf-8")
    print(out)

if __name__ == "__main__":
    main()
