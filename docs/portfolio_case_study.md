# Portfolio Case Study

## Problem

Build a transparent visual odometry and 3D reconstruction platform that exposes geometry, uncertainty, failure modes, scale limitations, and benchmark evidence.

## Why common CV demos are weak

Many demos show only object boxes, a final model prediction, or a fake dashboard. They do not prove geometry knowledge, reproducibility, diagnostics, or system design.

## What SceneMotion-3D proves

- geometry-based visual odometry
- feature matching and robust estimation
- triangulation and reprojection reasoning
- benchmark evaluation with ATE/RPE
- honest scale management
- backend/frontend engineering
- artifact tracking and reproducible demos

## Architecture decisions

A local-first FastAPI + Next.js architecture keeps the project easy to run while still showing production-style service boundaries.

## Hardest technical parts

- keeping monocular scale claims honest
- rejecting bad frame pairs without hiding failures
- generating inspectable evidence for each stage
- aligning trajectories for evaluation without confusing that with runtime scale recovery

## What a recruiter should notice

This project is not a wrapper. It demonstrates the core CV concepts behind robotics perception, SLAM, AR/VR tracking, and 3D reconstruction.

## Interview positioning

Describe it as a transparent VO/SfM-style platform that turns a video into keyframes, feature matches, relative trajectory, sparse/dense point clouds, reports, and benchmark metrics.
