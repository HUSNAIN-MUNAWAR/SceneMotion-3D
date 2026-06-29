# ADR: Use classical visual odometry as the core

## Context

Many CV portfolios rely on object detection or pretrained wrappers.

## Decision

Build the main pipeline around features, matching, essential matrix, pose recovery, and triangulation.

## Consequences

Shows geometry knowledge, but requires honest failure handling.

## Alternatives considered

YOLO/CCTV analytics, a single depth model, notebook-only demo.
