from pathlib import Path
import sys, json
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from vision_core.evaluation.benchmark_runner import generate_synthetic_benchmark, run_benchmark


def main():
    out = ROOT / 'outputs' / 'benchmark_demo'
    if out.exists():
        import shutil; shutil.rmtree(out)
    est, gt = generate_synthetic_benchmark(out)
    metrics = run_benchmark(est, gt, out)
    print(json.dumps(metrics, indent=2))

if __name__ == '__main__':
    main()
