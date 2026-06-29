from pathlib import Path
import sys
import argparse
import json
import shutil

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from workers.pipeline_worker import run_pipeline_job


def main(argv=None):
    parser = argparse.ArgumentParser(description='Run SceneMotion-3D demo pipeline.')
    parser.add_argument('--video', default=None, help='Optional custom MP4 path. Defaults to bundled synthetic video.')
    parser.add_argument('--out', default=None, help='Optional output directory.')
    parser.add_argument('--target-fps', type=float, default=4)
    parser.add_argument('--max-keyframes', type=int, default=12)
    parser.add_argument('--resize-width', type=int, default=640)
    args = parser.parse_args(argv)

    if args.video:
        video = Path(args.video).expanduser().resolve()
        if not video.exists():
            raise FileNotFoundError(f'Custom video not found: {video}')
        out = Path(args.out).expanduser().resolve() if args.out else ROOT / 'outputs' / 'demo_custom'
    else:
        video = ROOT / 'sample_data' / 'videos' / 'synthetic_scene.mp4'
        if not video.exists():
            from scripts.generate_sample_video import main as gen
            gen()
        out = ROOT / 'outputs' / 'demo_job_synthetic'

    if out.exists():
        shutil.rmtree(out)
    metrics = run_pipeline_job(video, out, {'target_fps': args.target_fps, 'max_keyframes': args.max_keyframes, 'resize_width': args.resize_width})
    print('Demo completed')
    print(out)
    print(json.dumps(metrics, indent=2, default=str))
    return metrics

if __name__ == '__main__':
    main()
