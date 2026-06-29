# Interview Guide

## 30-second explanation

SceneMotion-3D is a monocular visual odometry and 3D reconstruction platform. It extracts frames, selects keyframes, matches visual features, estimates relative camera motion, triangulates sparse 3D points, generates depth-assisted point clouds, evaluates trajectories with ATE/RPE when ground truth exists, and exports reports and artifact bundles.

## 2-minute explanation

The project demonstrates core geometry-based computer vision rather than object detection. I built a FastAPI backend, local worker pipeline, `vision_core` modules, and Next.js frontend. The pipeline performs feature extraction, RANSAC matching, essential matrix estimation, pose recovery, triangulation, depth provider abstraction, quality filtering, and benchmark evaluation. It also explains limitations like monocular scale ambiguity and low-parallax failure cases.

## Deep technical explanation

For each pair of keyframes, the system extracts ORB features, matches descriptors, filters outliers using RANSAC, estimates the essential matrix from normalized camera coordinates, and recovers relative rotation and translation direction. It chains relative poses into a trajectory and triangulates matched points. Reprojection error and inlier ratios are used as quality signals.

## Scale ambiguity explanation

A monocular camera cannot infer absolute metric scale from images alone. SceneMotion-3D defaults to relative scale and only uses scale references or ground-truth alignment when explicitly provided. Sim(3) alignment is used for evaluation only.

## ATE/RPE explanation

ATE measures global trajectory deviation after alignment. RPE measures local relative motion consistency between steps. They help evaluate VO behavior when ground-truth poses are available.

## Bundle adjustment explanation

The repository includes a small sliding-window least-squares refinement that minimizes reprojection residuals. It is educational and local, not a replacement for COLMAP/g2o/Ceres.

## Failure cases

Low texture, blur, pure rotation, repeated patterns, dynamic objects, rolling shutter, bad intrinsics, and insufficient parallax can all break monocular VO. The project reports warnings and recommended fixes.

## What I would improve next

Add stereo VO, IMU fusion, pose-graph optimization, real depth providers behind explicit setup, and COLMAP comparison workflows.

## Possible interviewer questions

**Q: Why not use YOLO?**  
A: The goal is geometry-based perception, not object detection.

**Q: Does it recover metric scale?**  
A: Not by default. Monocular VO is relative scale unless a scale source is provided.

**Q: Is this production SLAM?**  
A: No. It is production-style architecture and an educational/research portfolio platform, not a certified SLAM stack.
