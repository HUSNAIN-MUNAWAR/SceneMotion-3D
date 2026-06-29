# ADR: Maintain offline-safe demo mode

## Context

Recruiters may run the project without GPU or large datasets.

## Decision

Synthetic data and fallback providers are bundled.

## Consequences

Validation is reproducible on small machines.

## Alternatives considered

Requiring KITTI/TUM downloads by default.
