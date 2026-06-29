from __future__ import annotations
from pathlib import Path
from .base_dataset import DatasetMetadata, require_path


def prepare_kitti_dataset(sequence_path: str | Path, output_dir: str | Path, poses_file: str | Path | None = None) -> dict:
    src = require_path(sequence_path, 'KITTI sequence path')
    image_dir = src / 'image_0'
    if not image_dir.exists(): image_dir = src / 'image_2'
    warnings = [] if image_dir.exists() else ['Missing image_0/image_2 folder.']
    frame_count = len(list(image_dir.glob('*.png'))) if image_dir.exists() else 0
    pose = Path(poses_file) if poses_file else src / 'poses.txt'
    if not pose.exists(): warnings.append('Missing KITTI pose file; trajectory benchmark disabled.')
    meta = DatasetMetadata('kitti_odometry', str(src), str(image_dir) if image_dir.exists() else None, str(pose) if pose.exists() else None, frame_count, warnings)
    return {**meta.__dict__, 'metadata_path': meta.save(Path(output_dir) / 'dataset_metadata.json')}
