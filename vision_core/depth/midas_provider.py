from pathlib import Path
from .fallback_depth import FallbackDepthProvider

class MidasDepthProvider(FallbackDepthProvider):
    """Optional provider placeholder.

    A real deployment can replace this with torch hub / local weights loading. This class deliberately
    falls back unless explicit model code and weights are installed, avoiding surprise downloads.
    """
    name = "midas_optional_not_loaded"

    def __init__(self):
        super().__init__(reason="MiDaS weights are not bundled; fallback pseudo-depth used unless provider is implemented locally.")
