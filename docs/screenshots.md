# Screenshots

Screenshot assets live under `docs/screenshots/`.

They are now generated from the **real** `outputs/demo_job_synthetic` artifacts rather than generic placeholder cards.

The generator reads:

- `metrics.json`
- `trajectory.json`
- `pointclouds/sparse_cloud.json`
- `matches/*.jpg`
- `depth/*.png`
- artifact metadata from `artifacts.json`

Regenerate them with:

```bash
python scripts/generate_screenshots.py
```

Primary outputs include:

- `landing_page.png`
- `upload_page.png`
- `processing_page.png`
- `reconstruction_dashboard.png`
- `feature_matches.png`
- `depth_explorer.png`
- `pointcloud_viewer.png`
- `benchmark_report.png`
