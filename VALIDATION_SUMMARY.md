# Validation Summary - SceneMotion-3D Senior Upgrade

Validation date: 2026-06-28

## Commands executed

| Command | Result |
|---|---|
| `python -m compileall backend vision_core workers scripts` | Passed |
| `pytest tests -q` | 17 passed |
| `make test` | Passed, 17 tests |
| `python - <<'PY' from backend.app.main import app ...` | Passed, backend imported with 25 routes |
| `make demo` | Passed |
| `make benchmark-demo` | Passed |
| `make bundle-demo` | Passed |
| `make screenshots` | Passed, 8 generated UI preview screenshots |
| `node scripts/check_frontend.mjs` | Passed |
| `cd frontend && npm install` | Passed |
| `cd frontend && npm run typecheck` | Passed |
| `cd frontend && timeout 120s env NEXT_TELEMETRY_DISABLED=1 npm run build` | Passed |
| PDF render verification with `/home/oai/skills/pdfs/scripts/render_pdf.py` | Passed, 2 pages rendered |

## Demo metrics

| Metric | Value |
|---|---:|
| Extracted frames | 16 |
| Selected keyframes | 8 |
| Average keypoints/keyframe | 1638.125 |
| Average matches/pair | 532.5714 |
| Average inlier ratio | 0.6680 |
| Valid pose pairs | 7 |
| Sparse points | 3371 |
| Depth maps | 4 |
| Dense cloud points | 4240 |
| Scale mode | relative |
| Loop candidates | 4 |
| Verified loop candidates | 4 |
| Rejected pairs | 0 |

## Benchmark demo metrics

| Metric | Value |
|---|---:|
| Aligned trajectory pairs | 40 |
| Sim(3) scale, evaluation only | 1.6078117 |
| ATE RMSE | 0.0567718 |
| ATE mean | 0.0524366 |
| ATE max | 0.0982167 |
| RPE RMSE | 0.0802479 |
| RPE mean | 0.0743533 |
| RPE max | 0.1364513 |

## Generated artifacts

- `outputs/demo_job_synthetic/report.html`
- `outputs/demo_job_synthetic/report.pdf`
- `outputs/demo_job_synthetic/artifact_bundle.zip`
- `outputs/demo_job_synthetic/pointclouds/sparse_cloud.ply`
- `outputs/demo_job_synthetic/pointclouds/dense_cloud.ply`
- `outputs/benchmark_demo/benchmark_report.html`
- `outputs/benchmark_demo/trajectory_plot.png`
- `outputs/benchmark_demo/error_plot.png`
- `docs/screenshots/*.png`

## Honest limitations preserved

SceneMotion-3D estimates relative monocular trajectory by default. Absolute metric scale requires additional information such as known camera intrinsics, known object size, known camera height, stereo baseline, depth sensor, IMU, or ground-truth alignment for evaluation. Fallback pseudo-depth is provided for offline demonstration only and must not be interpreted as metric depth.
