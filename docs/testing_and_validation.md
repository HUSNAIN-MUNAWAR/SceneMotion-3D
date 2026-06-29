# Testing and Validation

Run the final validation stack:

```bash
python -m compileall backend vision_core workers scripts
make test
make demo
make benchmark-demo
make bundle-demo
make screenshots
make validate-final
cd frontend && npm install && npm run typecheck && npm run build
```

The machine-readable summary is written to:

```text
outputs/final_validation/validation_summary.json
```

The human-readable summary is `VALIDATION.md`.
