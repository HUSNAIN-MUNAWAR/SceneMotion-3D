from .parallax import estimate_parallax


def dynamic_scene_warning(image_a, image_b, high_motion_px: float = 80.0) -> dict:
    p = estimate_parallax(image_a, image_b)
    excessive = p.get('mean_flow', 0.0) > high_motion_px
    return {"dynamic_warning": bool(excessive), "reason": "excessive_or_inconsistent_motion" if excessive else "ok", **p}
