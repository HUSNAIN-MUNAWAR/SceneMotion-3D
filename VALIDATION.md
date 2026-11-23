# Final Validation

Generated: 2026-11-23T10:49:14+00:00

This release was validated with source checks, demo generation, benchmark generation, bundle export, real-data screenshot generation, and frontend static structure checks. Frontend typecheck/build were attempted but remain blocked by an incomplete `npm ci` under Node 24/npm 11.

## Commands run

```bash
py -3.12 -m compileall backend vision_core workers scripts
py -3.12 -m pytest tests -q
py -3.12 scripts/run_demo_pipeline.py
py -3.12 scripts/run_benchmark_demo.py
py -3.12 scripts/run_bundle_demo.py
py -3.12 scripts/generate_screenshots.py
node scripts/check_frontend.mjs
cd frontend && npm ci --no-audit --no-fund
cd frontend && npm run typecheck
cd frontend && npm run build
```

## Validation table

| Check | Result |
|---|---|
| Python compile | passed |
| Pytest | passed - 17 tests |
| Demo pipeline | passed |
| Benchmark demo | passed |
| Bundle demo | passed |
| Frontend static check | passed |
| Frontend typecheck | failed - incomplete npm install (`tsc` unavailable) |
| Frontend build | failed - incomplete npm install (`next` unavailable) |
| PDF report generated | True |
| PDF render verification | generated PDF exists; external renderer not run on this Windows host |
| Screenshots generated | True |
| Artifact bundle generated | True |
| Benchmark report generated | True |

## Demo metrics

| Metric | Value |
|---|---:|
| Extracted frames | 16 |
| Selected keyframes | 8 |
| Avg keypoints/keyframe | 1638.75 |
| Avg matches/pair | 536.2857142857143 |
| Avg inlier ratio | 0.6747085188644014 |
| Valid pose pairs | 7 |
| Rejected pairs | 0 |
| Sparse 3D points | 3468 |
| Depth maps | 4 |
| Dense cloud points | 4240 |
| Loop candidates | 4 |
| Verified loop candidates | 4 |

## Benchmark metrics

| Metric | Value |
|---|---:|
| Aligned trajectory pairs | 40 |
| ATE RMSE | 0.056771800117580366 |
| ATE mean | 0.05243662060155463 |
| ATE max | 0.09821669598766167 |
| RPE RMSE | 0.08024793955827417 |
| RPE mean | 0.07435325931646987 |
| RPE max | 0.13645125248401713 |

## Generated evidence

- `outputs/demo_job_synthetic/report.html`
- `outputs/demo_job_synthetic/report.pdf`
- `outputs/demo_job_synthetic/artifact_bundle.zip`
- `outputs/demo_job_synthetic/pointclouds/sparse_cloud.ply`
- `outputs/demo_job_synthetic/pointclouds/dense_cloud.ply`
- `outputs/benchmark_demo/benchmark_report.html`
- `outputs/benchmark_demo/trajectory_plot.png`
- `outputs/benchmark_demo/error_plot.png`
- `outputs/final_validation/validation_summary.json` (backend/artifact pass; frontend gates failed)
- `docs/screenshots/*.png`

## Notes

- `npm ci` stalled under Node 24/npm 11 and was stopped; direct typecheck/build then failed because the local frontend dependency tree was incomplete.
- The screenshots are generated from the real demo artifacts, but are not live browser captures.
- Monocular trajectory is relative scale by default.
- Sim(3) alignment is evaluation-only.
- Fallback pseudo-depth is not metric depth.
