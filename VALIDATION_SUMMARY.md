# Validation Summary - SceneMotion-3D Senior Upgrade

Validation date: 2026-11-23

## Commands executed

| Command | Result |
|---|---|
| `py -3.12 -m compileall backend vision_core workers scripts` | Passed |
| `py -3.12 -m pytest tests -q` | 17 passed |
| `py -3.12 scripts/run_demo_pipeline.py` | Passed; real pipeline artifacts regenerated |
| `py -3.12 scripts/run_benchmark_demo.py` | Passed; ATE/RPE artifacts regenerated |
| `py -3.12 scripts/run_bundle_demo.py` | Passed; 4,502,490-byte ZIP generated |
| `py -3.12 scripts/generate_screenshots.py` | Passed; 11 real-data PNGs regenerated |
| `node scripts/check_frontend.mjs` | Passed |
| `cd frontend && npm ci --no-audit --no-fund` | Stalled under Node 24/npm 11 and was stopped; dependency tree remained incomplete |
| `cd frontend && npm run typecheck` | Failed because `tsc` was unavailable after incomplete install |
| `cd frontend && npm run build` | Failed because the `next` executable was unavailable after incomplete install |
| `py -3.12 scripts/validate_final.py` | Expected non-zero release gate: backend/artifacts passed; frontend typecheck/build remained unavailable |

## Demo metrics

| Metric | Value |
|---|---:|
| Extracted frames | 16 |
| Selected keyframes | 8 |
| Average keypoints/keyframe | 1638.75 |
| Average matches/pair | 536.2857 |
| Average inlier ratio | 0.6747 |
| Valid pose pairs | 7 |
| Sparse points | 3468 |
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

SceneMotion-3D estimates relative monocular trajectory by default. Absolute metric scale requires additional information such as known camera intrinsics, known object size, known camera height, stereo baseline, depth sensor, IMU, or ground-truth alignment for evaluation. Fallback pseudo-depth is provided for offline demonstration only and must not be interpreted as metric depth. Frontend static structure is validated, but the frontend dependency installation/typecheck/build remains blocked by the incomplete npm install on this host.
