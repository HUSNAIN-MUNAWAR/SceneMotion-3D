def known_distance_scale(observed_relative_distance: float, known_metric_distance: float) -> dict:
    if observed_relative_distance <= 0 or known_metric_distance <= 0:
        return {"scale_factor": 1.0, "confidence": 0.0, "warnings": ["Invalid known-distance values; using relative scale."]}
    return {"scale_factor": float(known_metric_distance / observed_relative_distance), "confidence": 0.75, "warnings": ["Known-distance scale assumes the measured relative distance is reliable."]}
