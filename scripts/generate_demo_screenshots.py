from pathlib import Path
import json
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'docs' / 'screenshots'
OUT.mkdir(parents=True, exist_ok=True)

def _font(size=28):
    try:
        return ImageFont.truetype('DejaVuSans.ttf', size)
    except Exception:
        return ImageFont.load_default()

def card(draw, xy, title, body):
    x1,y1,x2,y2 = xy
    draw.rounded_rectangle(xy, radius=24, fill=(15,23,42), outline=(51,65,85), width=2)
    draw.text((x1+28,y1+24), title, font=_font(28), fill=(248,250,252))
    draw.multiline_text((x1+28,y1+70), body, font=_font(18), fill=(203,213,225), spacing=8)

def main():
    metrics_path = ROOT / 'outputs' / 'demo_job_synthetic' / 'metrics.json'
    metrics = json.loads(metrics_path.read_text()) if metrics_path.exists() else {}
    img = Image.new('RGB', (1400, 900), (2, 6, 23))
    d = ImageDraw.Draw(img)
    d.text((60,50), 'SceneMotion 3D - Demo Dashboard Snapshot', font=_font(44), fill=(255,255,255))
    card(d, (60,140,650,390), 'Reconstruction metrics', f"Keyframes: {metrics.get('selected_keyframes','-')}\nAvg keypoints: {metrics.get('average_keypoints_per_keyframe','-')}\nValid pose pairs: {metrics.get('valid_pose_pairs','-')}\nSparse points: {metrics.get('sparse_3d_point_count','-')}")
    card(d, (720,140,1340,390), 'Depth and dense cloud', f"Depth maps: {metrics.get('depth_maps_generated','-')}\nDense points: {metrics.get('dense_cloud_point_count','-')}\nProvider: {metrics.get('depth_provider','fallback')}")
    warnings = '\n'.join(f"- {w}" for w in metrics.get('warnings', [])[:5])
    card(d, (60,450,1340,820), 'Warnings and limitations', warnings or 'Warnings appear after a demo run.')
    out = OUT / 'dashboard_snapshot.png'
    img.save(out)
    print(out)

if __name__ == '__main__':
    main()
