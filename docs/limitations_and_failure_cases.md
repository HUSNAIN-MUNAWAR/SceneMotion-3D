# Limitations and Failure Cases

SceneMotion-3D does not hide failure modes. It reports warning signals and recommended fixes.

| Failure case | Signal | Recommended fix |
|---|---|---|
| Low texture | few keypoints | record textured surfaces |
| Motion blur | low Laplacian sharpness | slower movement, better lighting |
| Pure rotation | weak parallax | translate the camera, not only rotate |
| Dynamic scene | inconsistent optical flow | reduce moving people/cars or mask them |
| Bad intrinsics | projection warnings | provide calibration JSON |
| Scale ambiguity | relative scale mode | provide known distance, RGB-D, stereo, IMU, or ground truth for evaluation |

Fallback pseudo-depth exists only to keep the demo offline-safe. It is not metric depth.
