from __future__ import annotations
from pathlib import Path
from .base_dataset import DatasetMetadata, require_path


def prepare_tum_dataset(dataset_path: str | Path, output_dir: str | Path) -> dict:
    src = require_path(dataset_path, 'TUM dataset path')
    rgb_txt = src / 'rgb.txt'; gt_txt = src / 'groundtruth.txt'
    warnings = []
    if not rgb_txt.exists(): warnings.append('Missing rgb.txt; provide a standard TUM RGB-D folder.')
    if not gt_txt.exists(): warnings.append('Missing groundtruth.txt; benchmark will be unavailable.')
    frame_count = 0
    if rgb_txt.exists():
        frame_count = sum(1 for line in rgb_txt.read_text(encoding='utf-8', errors='ignore').splitlines() if line.strip() and not line.startswith('#'))
    meta = DatasetMetadata('tum_rgbd', str(src), str(src), str(gt_txt) if gt_txt.exists() else None, frame_count, warnings)
    return {**meta.__dict__, 'metadata_path': meta.save(Path(output_dir) / 'dataset_metadata.json')}
