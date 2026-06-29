from __future__ import annotations
from pathlib import Path
from .fallback_depth import FallbackDepthProvider
from .external_depth_provider import ExternalDepthProvider
from .rgbd_depth_provider import RGBDDepthProvider

class DepthProviderRegistry:
    def __init__(self):
        self._providers = {
            'fallback': FallbackDepthProvider,
            'fallback_pseudo_depth': FallbackDepthProvider,
            'external': ExternalDepthProvider,
            'rgbd': RGBDDepthProvider,
        }

    def available(self):
        return sorted(self._providers.keys() | {'midas_optional', 'depth_anything_optional'})

    def create(self, name: str = 'fallback', **kwargs):
        key = (name or 'fallback').lower()
        if key in {'midas', 'depth_anything'}:
            raise RuntimeError(f'{key} provider is optional and is not auto-downloaded. Configure weights/dependencies explicitly.')
        cls = self._providers.get(key)
        if cls is None:
            raise KeyError(f'Unknown depth provider: {name}')
        return cls(**kwargs)
