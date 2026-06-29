# API Reference

Base URL: `http://localhost:8000`

## Health

| Method | Path | Purpose |
|---|---|---|
| GET | `/api/health` | service status and dependency notes |

Example:

```bash
curl http://localhost:8000/api/health
```

Response:

```json
{"status":"ok","service":"SceneMotion 3D","dependencies":{"opencv":"required","redis":"optional"}}
```

## Video endpoints

| Method | Path | Purpose |
|---|---|---|
| POST | `/api/videos/upload` | upload a validated MP4 video |
| GET | `/api/videos/samples` | list bundled sample videos |

## Job lifecycle

| Method | Path | Purpose |
|---|---|---|
| POST | `/api/jobs/start` | create and start a job |
| GET | `/api/jobs/{job_id}` | job status |
| POST | `/api/jobs/{job_id}/cancel` | request cancellation |
| DELETE | `/api/jobs/{job_id}` | remove in-memory job record |
| WS | `/api/jobs/{job_id}/stream` | progress stream |

Start sample job:

```bash
curl -X POST http://localhost:8000/api/jobs/start \
  -H "Content-Type: application/json" \
  -d '{"source":"sample","sample_name":"synthetic_scene.mp4","config":{"target_fps":4}}'
```

Job status response:

```json
{
  "job_id": "...",
  "status": "running",
  "progress": 45,
  "stage": "feature_matching",
  "message": "matching keyframes",
  "warnings": []
}
```

## Artifacts

| Method | Path | Purpose |
|---|---|---|
| GET | `/api/jobs/{job_id}/metrics` | numeric metrics |
| GET | `/api/jobs/{job_id}/artifacts` | artifact listing |
| GET | `/api/jobs/{job_id}/frames` | frame list |
| GET | `/api/jobs/{job_id}/trajectory` | relative trajectory JSON |
| GET | `/api/jobs/{job_id}/pointcloud?dense=false` | sparse PLY |
| GET | `/api/jobs/{job_id}/pointcloud?dense=true` | dense PLY |
| GET | `/api/jobs/{job_id}/report?fmt=html` | HTML report |
| GET | `/api/jobs/{job_id}/report?fmt=pdf` | PDF report |
| GET | `/api/jobs/{job_id}/bundle` | artifact bundle ZIP |

## Experiments and config

| Method | Path | Purpose |
|---|---|---|
| GET | `/api/experiments` | list runs |
| GET | `/api/experiments/{run_id}` | get one run |
| POST | `/api/experiments/compare` | compare runs |
| GET | `/api/config/presets` | list pipeline presets |

## Error response format

FastAPI returns standard JSON errors:

```json
{"detail":"Job not found"}
```

Client code should display these errors instead of silently failing.
