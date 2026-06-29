# Visual Odometry Theory

The pipeline matches features between adjacent keyframes, estimates the essential matrix with RANSAC, recovers relative rotation and translation direction, then chains relative poses. Translation magnitude remains ambiguous in monocular vision.
