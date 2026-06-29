# Benchmarking

Benchmark mode compares an estimated trajectory against ground truth.

```mermaid
flowchart TD
    Estimated[Estimated trajectory] --> Align[Timestamp alignment]
    GroundTruth[Ground truth trajectory] --> Align
    Align --> Sim3[Sim(3) alignment for evaluation only]
    Sim3 --> ATE[Absolute Trajectory Error]
    Sim3 --> RPE[Relative Pose Error]
    ATE --> Report[Benchmark report]
    RPE --> Report
```

Important: Sim(3) alignment is an evaluation technique. It does not mean monocular VO recovered metric scale at runtime.

Included synthetic benchmark metrics:

| Metric | Value |
|---|---:|
| Aligned pairs | 40 |
| ATE RMSE | 0.056771800117580366 |
| RPE RMSE | 0.08024793955827417 |

Run:

```bash
make benchmark-demo
```
