# Final Validation

Generated: 2026-06-28T20:38:19.494275+00:00

This release was validated with source checks, demo generation, benchmark generation, bundle export, UI screenshot generation, frontend typecheck/build, and PDF render verification.

## Commands run

```bash
python -m compileall backend vision_core workers scripts
make test
make demo
make benchmark-demo
make bundle-demo
make screenshots
cd frontend && npm install && npm run typecheck && npm run build
make validate-final
python /home/oai/skills/pdfs/scripts/render_pdf.py outputs/demo_job_synthetic/report.pdf --out_dir /mnt/data/scenemotion_final_pdf_render --dpi 140
```

## Validation table

| Check | Result |
|---|---|
| Python compile | passed |
| Pytest | passed - 17 tests |
| Demo pipeline | passed |
| Benchmark demo | passed |
| Bundle demo | passed |
| Frontend typecheck | passed |
| Frontend build | passed |
| PDF report generated | True |
| PDF render verification | passed - 2 pages rendered |
| Screenshots generated | True |
| Artifact bundle generated | True |
| Benchmark report generated | True |

## Demo metrics

| Metric | Value |
|---|---:|
| Extracted frames | 16 |
| Selected keyframes | 8 |
| Avg keypoints/keyframe | 1638.125 |
| Avg matches/pair | 532.5714285714286 |
| Avg inlier ratio | 0.6680122740205736 |
| Valid pose pairs | 7 |
| Rejected pairs | 0 |
| Sparse 3D points | 3371 |
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
- `outputs/final_validation/validation_summary.json`
- `docs/screenshots/*.png`

## Notes

- `npm install` completed and reported 2 moderate dependency audit warnings from the frontend dependency tree. The release validation typecheck/build still passed.
- The screenshots are generated UI preview assets unless a live browser capture workflow is added later.
- Monocular trajectory is relative scale by default.
- Sim(3) alignment is evaluation-only.
- Fallback pseudo-depth is not metric depth.
