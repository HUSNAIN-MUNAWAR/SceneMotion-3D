import numpy as np
from vision_core.evaluation.alignment import sim3_umeyama


def ground_truth_scale(est_positions, gt_positions) -> dict:
    result = sim3_umeyama(np.asarray(est_positions), np.asarray(gt_positions), with_scale=True)
    return {"scale_factor": result["scale"], "confidence": 1.0, "warnings": ["Ground-truth scale is evaluation-only and must not be used as runtime metric scale."]}
