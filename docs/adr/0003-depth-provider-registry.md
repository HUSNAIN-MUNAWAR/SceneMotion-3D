# ADR: Use a depth provider registry

## Context

Depth models may require large weights and online downloads.

## Decision

Provide offline fallback pseudo-depth and optional provider hooks.

## Consequences

Demo always runs; real providers can be added later.

## Alternatives considered

Hard dependency on a huge pretrained model.
