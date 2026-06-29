from pathlib import Path
import sys, json
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from vision_core.artifacts.bundle_exporter import create_artifact_bundle
from scripts.run_demo_pipeline import main as run_demo


def main():
    demo_dir = ROOT / 'outputs' / 'demo_job_synthetic'
    if not (demo_dir / 'metrics.json').exists():
        run_demo()
    bundle = create_artifact_bundle(demo_dir, demo_dir / 'artifact_bundle.zip')
    print(json.dumps({'bundle': bundle, 'exists': Path(bundle).exists(), 'size_bytes': Path(bundle).stat().st_size}, indent=2))

if __name__ == '__main__':
    main()
