from pathlib import Path
from vision_core.evaluation.benchmark_runner import generate_synthetic_benchmark, run_benchmark


def test_benchmark_demo_generates_metrics(tmp_path):
    est, gt = generate_synthetic_benchmark(tmp_path, n=12)
    metrics = run_benchmark(est, gt, tmp_path)
    assert metrics['aligned_pairs'] == 12
    assert metrics['ate']['rmse'] < 0.2
    assert (tmp_path / 'trajectory_plot.png').exists()
    assert (tmp_path / 'benchmark_report.html').exists()
