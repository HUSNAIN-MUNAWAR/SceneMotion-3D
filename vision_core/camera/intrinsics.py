from dataclasses import dataclass, asdict
import numpy as np

@dataclass
class CameraIntrinsics:
    fx: float
    fy: float
    cx: float
    cy: float
    width: int
    height: int
    source: str = "estimated"

    @property
    def K(self):
        return np.array([[self.fx, 0, self.cx], [0, self.fy, self.cy], [0, 0, 1]], dtype=np.float64)

    def to_dict(self):
        data = asdict(self)
        data["warning"] = "Approximate intrinsics affect motion, triangulation, and cloud quality." if self.source == "estimated" else "Provided intrinsics used."
        return data


def estimate_intrinsics(width: int, height: int, focal_factor: float = 1.2) -> CameraIntrinsics:
    focal = focal_factor * max(width, height)
    return CameraIntrinsics(fx=focal, fy=focal, cx=width / 2.0, cy=height / 2.0, width=width, height=height, source="estimated")
