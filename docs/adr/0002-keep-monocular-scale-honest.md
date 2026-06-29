# ADR: Keep monocular scale honest

## Context

Monocular video cannot recover absolute metric scale without references.

## Decision

Default to relative scale and expose scale modes explicitly.

## Consequences

Avoids fake claims and teaches reviewers the real limitation.

## Alternatives considered

Pretending translation units are meters.
