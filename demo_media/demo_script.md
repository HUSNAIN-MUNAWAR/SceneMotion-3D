# 2-Minute Demo Script

**0:00 - Problem statement**  
Most computer vision demos show a final prediction but hide the geometry and failure modes. SceneMotion-3D exposes the visual odometry pipeline end to end.

**0:15 - Upload/sample video**  
Select the bundled synthetic sample or upload your own MP4. The system extracts frames and selects keyframes.

**0:30 - Pipeline stages**  
Show keyframes, feature extraction, feature matching, RANSAC inliers, and rejected-pair warnings.

**0:50 - Feature matching and trajectory**  
Explain essential matrix estimation, recoverPose, pose chaining, and relative monocular scale.

**1:10 - Point cloud/depth**  
Show sparse triangulated points and dense depth-assisted point cloud. Mention fallback pseudo-depth is not metric.

**1:25 - Benchmark metrics**  
Open the benchmark report and explain ATE/RPE. Sim(3) alignment is for evaluation only.

**1:40 - Report/artifact bundle**  
Show the PDF report and artifact bundle ZIP with metrics, plots, point clouds, warnings, and configs.

**1:55 - Limitations**  
Close with honest limitations: scale ambiguity, blur, pure rotation, dynamic objects, and low texture.
