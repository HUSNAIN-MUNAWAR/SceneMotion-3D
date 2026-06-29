from __future__ import annotations
from dataclasses import dataclass, asdict
from .known_distance import known_distance_scale
from .depth_assisted_scale import depth_assisted_scale

@dataclass
class ScaleResult:
    mode: str
    scale_source: str
    scale_factor: float
    confidence: float
    limitations: list[str]
    warnings: list[str]

    def to_dict(self):
        return asdict(self)

class ScaleManager:
    def resolve(self, mode: str = 'relative', **kwargs) -> ScaleResult:
        mode = (mode or 'relative').lower()
        if mode in {'relative', 'relative_mono', 'relative_monocular'}:
            return ScaleResult('relative', 'monocular_relative_units', 1.0, 0.3, ['Absolute metric scale is unknown from monocular video alone.'], ['Relative scale only. Provide known distance, camera height, stereo/RGB-D, IMU, or ground truth for evaluation.'])
        if mode == 'known_distance':
            r = known_distance_scale(float(kwargs.get('observed_relative_distance', 0)), float(kwargs.get('known_metric_distance', 0)))
            return ScaleResult(mode, 'known_distance_reference', r['scale_factor'], r['confidence'], ['Assumes the selected reference distance is correctly measured.'], r['warnings'])
        if mode == 'camera_height':
            observed = float(kwargs.get('observed_camera_height_units', 0)); real = float(kwargs.get('known_camera_height_m', 0))
            if observed <= 0 or real <= 0:
                return ScaleResult(mode, 'invalid_camera_height_reference', 1.0, 0.0, ['Camera height reference is unavailable or invalid.'], ['Using relative scale.'])
            return ScaleResult(mode, 'known_camera_height', real/observed, 0.55, ['Ground plane and camera height assumptions can be wrong.'], ['Camera-height scale is approximate.'])
        if mode == 'rgbd_depth':
            r = depth_assisted_scale(float(kwargs.get('relative_depth_median', 0)), float(kwargs.get('metric_depth_median', 0)))
            return ScaleResult(mode, 'rgbd_or_external_depth', r['scale_factor'], r['confidence'], ['Depth quality and alignment control scale quality.'], r['warnings'])
        if mode == 'stereo_baseline_future':
            return ScaleResult(mode, 'future_work', 1.0, 0.0, ['Stereo baseline scale is listed as future work unless a stereo pipeline is implemented.'], ['Stereo baseline mode is not active in offline demo.'])
        if mode == 'ground_truth_aligned':
            return ScaleResult(mode, 'evaluation_only_ground_truth_alignment', float(kwargs.get('scale_factor', 1.0)), 1.0, ['Evaluation-only: not available for real runtime scale recovery.'], ['Do not report this as recovered metric scale.'])
        return ScaleResult(mode, 'unknown', 1.0, 0.0, ['Unknown scale mode.'], ['Using relative scale.'])
