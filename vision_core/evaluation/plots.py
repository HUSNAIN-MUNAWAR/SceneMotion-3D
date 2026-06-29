from __future__ import annotations
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import numpy as np


def _norm_xy(points, w=900, h=560, margin=60):
    pts = np.asarray(points, dtype=float)
    if pts.size == 0:
        return []
    xy = pts[:, [0, 2]] if pts.shape[1] >= 3 else pts[:, :2]
    mn = xy.min(axis=0); mx = xy.max(axis=0)
    scale = min((w-2*margin)/max(mx[0]-mn[0], 1e-9), (h-2*margin)/max(mx[1]-mn[1], 1e-9))
    px = (xy[:,0]-mn[0])*scale + margin
    py = h - ((xy[:,1]-mn[1])*scale + margin)
    return list(zip(px.tolist(), py.tolist()))


def draw_trajectory_plot(gt, aligned_est, output_path: str | Path) -> str:
    output_path = Path(output_path); output_path.parent.mkdir(parents=True, exist_ok=True)
    img = Image.new('RGB', (900, 560), 'white'); d = ImageDraw.Draw(img)
    d.rectangle([25,25,875,535], outline=(220,220,220))
    gt_pts = _norm_xy(gt); est_pts = _norm_xy(aligned_est)
    if len(gt_pts) > 1: d.line(gt_pts, fill=(30,120,220), width=4)
    if len(est_pts) > 1: d.line(est_pts, fill=(230,90,40), width=3)
    d.text((45,35), 'Trajectory plot (X-Z plane): blue=ground truth, orange=Sim(3)-aligned estimate', fill=(20,20,20))
    img.save(output_path)
    return str(output_path)


def draw_error_plot(errors, output_path: str | Path) -> str:
    output_path = Path(output_path); output_path.parent.mkdir(parents=True, exist_ok=True)
    img = Image.new('RGB', (900, 420), 'white'); d = ImageDraw.Draw(img)
    d.rectangle([45,45,860,360], outline=(220,220,220))
    errs = np.asarray(errors, dtype=float).ravel()
    if len(errs) > 1:
        xs = np.linspace(55, 850, len(errs))
        mx = max(float(errs.max()), 1e-9)
        ys = 350 - (errs / mx) * 290
        d.line(list(zip(xs.tolist(), ys.tolist())), fill=(180,40,60), width=3)
        d.text((55,370), f'max error={mx:.4f}', fill=(20,20,20))
    d.text((55,20), 'ATE per aligned timestamp', fill=(20,20,20))
    img.save(output_path)
    return str(output_path)
