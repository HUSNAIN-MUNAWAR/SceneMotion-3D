# LinkedIn Post Draft

I built SceneMotion-3D, a core computer vision portfolio project for monocular visual odometry, trajectory evaluation, and 3D reconstruction.

Instead of another object-detection dashboard, this project focuses on geometry: feature matching, RANSAC, essential matrix estimation, recoverPose, triangulation, reprojection error, scale ambiguity handling, ATE/RPE benchmark evaluation, depth-assisted point clouds, and artifact/report generation.

The repo includes FastAPI, Next.js, Docker, tests, synthetic demo data, benchmark outputs, generated reports, and honest limitations.

Key point: it estimates relative monocular trajectory by default. Metric scale requires a real scale reference such as stereo/RGB-D/IMU/known distance/ground truth for evaluation.
