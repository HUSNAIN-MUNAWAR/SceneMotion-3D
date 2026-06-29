from abc import ABC, abstractmethod
from pathlib import Path
import numpy as np

class DepthProvider(ABC):
    name = "base"

    @abstractmethod
    def predict(self, image_path: str | Path) -> dict:
        raise NotImplementedError


def get_depth_provider(name: str = "fallback"):
    if name.lower() == "midas":
        try:
            from .midas_provider import MidasDepthProvider
            return MidasDepthProvider()
        except Exception:
            from .fallback_depth import FallbackDepthProvider
            return FallbackDepthProvider(reason="MiDaS provider unavailable; using offline-safe fallback.")
    from .fallback_depth import FallbackDepthProvider
    return FallbackDepthProvider()
