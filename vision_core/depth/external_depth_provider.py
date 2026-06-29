from pathlib import Path
import numpy as np
from PIL import Image

class ExternalDepthProvider:
    name = 'external_depth_input'
    is_metric = False
    def __init__(self, depth_path: str | None = None):
        self.depth_path = Path(depth_path) if depth_path else None
    def estimate(self, frame_path: str):
        if self.depth_path is None or not self.depth_path.exists():
            raise FileNotFoundError('External depth path is required')
        if self.depth_path.suffix.lower() == '.npy':
            depth = np.load(self.depth_path).astype('float32')
        else:
            depth = np.asarray(Image.open(self.depth_path).convert('F'), dtype='float32')
        conf = np.ones_like(depth, dtype='float32') * 0.5
        return {"depth": depth, "confidence": conf, "warning": "External depth scale depends on the supplied file."}
