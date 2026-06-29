from __future__ import annotations
from pathlib import Path
from .base_dataset import DatasetMetadata, require_path


def prepare_euroc_dataset(dataset_path: str | Path, output_dir: str | Path) -> dict:
    src = require_path(dataset_path, 'EuRoC dataset path')
    cam = src / 'mav0' / 'cam0' / 'data'
    gt = src / 'mav0' / 'state_groundtruth_estimate0' / 'data.csv'
    warnings = []
    if not cam.exists(): warnings.append('Missing mav0/cam0/data image folder.')
    if not gt.exists(): warnings.append('Missing EuRoC ground-truth CSV.')
    frame_count = len(list(cam.glob('*.png'))) if cam.exists() else 0
    meta = DatasetMetadata('euroc_mav', str(src), str(cam) if cam.exists() else None, str(gt) if gt.exists() else None, frame_count, warnings)
    return {**meta.__dict__, 'metadata_path': meta.save(Path(output_dir) / 'dataset_metadata.json')}
