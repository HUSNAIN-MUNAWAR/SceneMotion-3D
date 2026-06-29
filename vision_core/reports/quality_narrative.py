def build_quality_narrative(metrics: dict) -> dict:
    warnings = metrics.get('warnings', [])
    quality = 'strong' if len(warnings) <= 2 and metrics.get('average_inlier_ratio', 0) > 0.45 else 'limited' if len(warnings) >= 5 else 'moderate'
    fixes = []
    if metrics.get('average_keypoints_per_keyframe', 0) < 120: fixes.append('Add texture or improve lighting.')
    if metrics.get('average_matches_per_pair', 0) < 40: fixes.append('Move camera more slowly and avoid motion blur.')
    if metrics.get('average_inlier_ratio', 0) < 0.3: fixes.append('Avoid repeated patterns and dynamic objects.')
    if metrics.get('intrinsics_source') == 'estimated': fixes.append('Provide a camera calibration JSON.')
    fixes.extend(['Use known scale reference, RGB-D, stereo, or IMU for metric scale.', 'Avoid pure rotation; add translation/parallax.'])
    return {"reconstruction_quality_grade": quality, "tracking_stability": metrics.get('average_inlier_ratio', 0), "scale_mode": metrics.get('scale_mode', 'relative'), "likely_failure_reasons": warnings, "recommended_fixes": sorted(set(fixes))}
