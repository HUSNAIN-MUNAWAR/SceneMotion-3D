from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'docs' / 'screenshots'
OUT.mkdir(parents=True, exist_ok=True)

SCREENS = [
    ('landing_page.png', 'Landing Page', ['Core CV / SLAM portfolio overview', 'Architecture diagrams', 'Honest scale disclaimer']),
    ('upload_page.png', 'Upload / Dataset Select', ['Sample video selector', 'Scale mode selector', 'Pipeline preset selector']),
    ('processing_page.png', 'Processing Job Page', ['WebSocket or polling progress', 'Current stage', 'Warnings as they appear']),
    ('reconstruction_dashboard.png', 'Reconstruction Dashboard', ['Metrics cards', 'Quality score', 'Artifact downloads']),
    ('feature_matches.png', 'Feature Match Viewer', ['Feature count per keyframe', 'Match visualization', 'RANSAC inlier ratio']),
    ('depth_explorer.png', 'Depth Explorer', ['Fallback pseudo-depth label', 'Depth provider registry', 'NPY/PNG outputs']),
    ('pointcloud_viewer.png', 'Trajectory + Point Cloud Viewer', ['Sparse/dense toggle', 'Trajectory toggle', 'Relative scale warning']),
    ('benchmark_report.png', 'Benchmark Results', ['ATE/RPE metrics', 'Trajectory plot', 'Evaluation-only Sim(3) note']),
    ('run_comparison.png', 'Run Comparison', ['Metric deltas', 'Timing profile', 'Quality warnings']),
    ('pdf_report_preview.png', 'PDF Report Preview', ['Quality narrative', 'Failure reasons', 'Recommended fixes']),
    ('artifact_bundle.png', 'Artifact Bundle', ['metrics.json', 'reports', 'point clouds', 'README_RUN.md']),
]

# Backward-compatible aliases used by earlier docs.
ALIASES = {
    'dashboard.png': 'reconstruction_dashboard.png',
    'trajectory_viewer.png': 'pointcloud_viewer.png',
    'dashboard_snapshot.png': 'reconstruction_dashboard.png',
}

def draw_card(path: Path, title: str, rows: list[str]) -> None:
    img = Image.new('RGB', (1400, 860), (9, 14, 26))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([44, 40, 1356, 820], radius=30, fill=(15, 23, 42), outline=(51, 65, 85), width=3)
    d.text((88, 80), 'SceneMotion-3D', fill=(147, 197, 253))
    d.text((88, 128), title, fill=(248, 250, 252))
    d.line([88, 178, 1310, 178], fill=(51, 65, 85), width=2)
    y = 220
    for row in rows:
        d.rounded_rectangle([88, y, 1312, y + 82], radius=18, fill=(30, 41, 59), outline=(71, 85, 105), width=2)
        d.text((124, y + 29), row, fill=(226, 232, 240))
        y += 112
    d.rounded_rectangle([88, 705, 1312, 770], radius=16, fill=(7, 89, 133), outline=(56, 189, 248), width=2)
    d.text((124, 728), 'Generated UI preview asset. Run frontend locally to capture live browser screenshots.', fill=(224, 242, 254))
    img.save(path)

for name, title, rows in SCREENS:
    draw_card(OUT / name, title, rows)
for alias, target in ALIASES.items():
    src = OUT / target
    dst = OUT / alias
    if src.exists():
        dst.write_bytes(src.read_bytes())
print(f'Generated {len(SCREENS)} required UI preview screenshots in {OUT}')
