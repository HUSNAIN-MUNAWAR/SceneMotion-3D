from __future__ import annotations
from pathlib import Path
from dataclasses import dataclass
import yaml
from .extractors import FeatureExtractor

@dataclass
class FeaturePipelineConfig:
    name: str
    feature_method: str = 'ORB'
    matcher: str = 'BFMatcher'
    ratio: float = 0.82
    cross_check: bool = False
    tracking: str | None = None
    max_features: int = 2000


def load_pipeline_config(path: str | Path) -> FeaturePipelineConfig:
    data = yaml.safe_load(Path(path).read_text(encoding='utf-8')) or {}
    return FeaturePipelineConfig(**{**{'name': Path(path).stem}, **data})


def load_available_presets(config_dir: str | Path) -> list[dict]:
    presets = []
    for p in sorted(Path(config_dir).glob('*.yaml')):
        cfg = load_pipeline_config(p)
        presets.append({"name": cfg.name, "feature_method": cfg.feature_method, "matcher": cfg.matcher, "tracking": cfg.tracking, "path": str(p)})
    return presets


def create_feature_extractor(config: FeaturePipelineConfig | dict) -> FeatureExtractor:
    if isinstance(config, dict): config = FeaturePipelineConfig(**config)
    return FeatureExtractor(config.feature_method, config.max_features)
