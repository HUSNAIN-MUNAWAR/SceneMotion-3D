# Depth Provider Registry

SceneMotion-3D implements this module in code and keeps demo mode offline-safe. The implementation is intentionally honest: monocular VO is relative-scale by default, Sim(3) alignment is evaluation-only, and optional external datasets or depth providers are not bundled as large downloads.

## Implemented

- Runnable Python module and tests where applicable.
- JSON artifacts written under `outputs/`.
- Failure cases and warnings surfaced in metrics/reports.

## Limitations

This project is a professional portfolio platform, not a claim of state-of-the-art SLAM. For industrial SfM/SLAM, compare with mature systems such as COLMAP, ORB-SLAM family, VINS, or OpenVSLAM-style systems.
