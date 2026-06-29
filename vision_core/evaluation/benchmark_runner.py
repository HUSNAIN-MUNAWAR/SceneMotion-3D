from __future__ import annotations
from pathlib import Path
import json
import numpy as np
from .trajectory_io import load_trajectory, save_tum_trajectory, align_by_timestamp
from .alignment import sim3_umeyama
from .ate import absolute_trajectory_error
from .rpe import relative_pose_error
from .plots import draw_trajectory_plot, draw_error_plot


def generate_synthetic_benchmark(out_dir: str | Path, n: int = 40) -> tuple[str, str]:
    out = Path(out_dir); out.mkdir(parents=True, exist_ok=True)
    ts = np.arange(n, dtype=float) * 0.1
    gt = np.stack([np.sin(ts)*2.0, 0.05*np.cos(ts*0.7), ts*0.8], axis=1)
    rng = np.random.default_rng(7)
    est = gt * 0.62 + np.array([0.2, -0.05, 0.12]) + rng.normal(0, 0.025, gt.shape)
    gt_path = save_tum_trajectory(out / 'ground_truth_trajectory.txt', ts, gt)
    est_path = save_tum_trajectory(out / 'estimated_trajectory.txt', ts, est)
    return est_path, gt_path


def run_benchmark(estimated_path: str | Path, ground_truth_path: str | Path, output_dir: str | Path, timestamp_tolerance: float | None = None) -> dict:
    out = Path(output_dir); out.mkdir(parents=True, exist_ok=True)
    est = load_trajectory(estimated_path)
    gt = load_trajectory(ground_truth_path)
    e_pos, g_pos, deltas = align_by_timestamp(est, gt, timestamp_tolerance)
    if len(e_pos) < 3:
        raise ValueError('Benchmark requires at least three aligned poses')
    sim3 = sim3_umeyama(e_pos, g_pos, with_scale=True)
    ate = absolute_trajectory_error(sim3['aligned'], g_pos)
    rpe = relative_pose_error(sim3['aligned'], g_pos, delta=1)
    (out / 'ate_metrics.json').write_text(json.dumps({k:v for k,v in ate.items() if k != 'errors'}, indent=2), encoding='utf-8')
    (out / 'rpe_metrics.json').write_text(json.dumps({k:v for k,v in rpe.items() if k != 'errors'}, indent=2), encoding='utf-8')
    draw_trajectory_plot(g_pos, sim3['aligned'], out / 'trajectory_plot.png')
    draw_error_plot(ate['errors'], out / 'error_plot.png')
    report = f"""<!doctype html><html><head><meta charset='utf-8'><title>SceneMotion Benchmark</title>
<style>body{{font-family:Inter,Arial,sans-serif;background:#0f172a;color:#e5e7eb;padding:40px}}.card{{background:#111827;border:1px solid #334155;border-radius:18px;padding:24px;margin:16px 0}}code{{color:#93c5fd}}</style></head>
<body><h1>SceneMotion-3D Benchmark Report</h1><div class='card'><h2>Evaluation-only Sim(3) Alignment</h2><p>Scale factor <code>{sim3['scale']:.6f}</code> was estimated only for comparison against ground truth. It is not runtime metric scale recovery.</p></div>
<div class='card'><h2>ATE</h2><p>RMSE: {ate['rmse']:.6f}, mean: {ate['mean']:.6f}, max: {ate['max']:.6f}, pairs: {ate['count']}</p></div>
<div class='card'><h2>RPE</h2><p>RMSE: {rpe['rmse']:.6f}, mean: {rpe['mean']:.6f}, max: {rpe['max']:.6f}, pairs: {rpe['count']}</p></div>
<img src='trajectory_plot.png' style='max-width:100%'><img src='error_plot.png' style='max-width:100%'></body></html>"""
    (out / 'benchmark_report.html').write_text(report, encoding='utf-8')
    return {"aligned_pairs": int(len(e_pos)), "sim3_scale_evaluation_only": sim3['scale'], "ate": {k:v for k,v in ate.items() if k != 'errors'}, "rpe": {k:v for k,v in rpe.items() if k != 'errors'}, "note": sim3['note'], "output_dir": str(out)}
