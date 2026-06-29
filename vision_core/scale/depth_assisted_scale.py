def depth_assisted_scale(relative_depth_median: float, metric_depth_median: float) -> dict:
    if relative_depth_median <= 0 or metric_depth_median <= 0:
        return {"scale_factor": 1.0, "confidence": 0.0, "warnings": ["Invalid depth medians; keeping relative scale."]}
    return {"scale_factor": float(metric_depth_median / relative_depth_median), "confidence": 0.6, "warnings": ["Depth-assisted scale depends on depth-map quality and camera calibration."]}
