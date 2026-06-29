# Architecture

SceneMotion-3D is split into a frontend, backend, local worker, and `vision_core` package. The backend owns job lifecycle, input validation, artifacts, and API responses. The worker calls the geometry pipeline. The frontend reads real API state and artifacts.

```mermaid
flowchart LR
    Frontend[Next.js UI] --> Backend[FastAPI]
    Backend --> Worker[Local pipeline worker]
    Worker --> Core[vision_core]
    Core --> Outputs[(outputs/job_id)]
    Outputs --> Reports[HTML/PDF reports]
    Outputs --> Bundle[artifact_bundle.zip]
    Backend --> Registry[Experiment registry]
```

The design is production-style but intentionally local-first. Redis and Docker Compose are included, but the default demo remains offline-safe and lightweight.
