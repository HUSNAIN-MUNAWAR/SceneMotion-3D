from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.core.config import get_settings
from backend.app.api.video_api import router as video_router
from backend.app.api.jobs_api import router as jobs_router
from backend.app.api.artifacts_api import router as artifacts_router
from backend.app.api.experiments_api import router as experiments_router
from backend.app.api.config_api import router as config_router

settings = get_settings()
app = FastAPI(title="SceneMotion 3D API", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in settings.cors_origins.split(",") if o.strip()],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health", tags=["health"])
@app.get("/api/health", tags=["health"])
def health():
    return {"status": "ok", "service": "SceneMotion 3D", "dependencies": {"opencv": "required", "redis": "optional"}}

app.include_router(video_router)
app.include_router(jobs_router)
app.include_router(artifacts_router)

app.include_router(experiments_router)
app.include_router(config_router)
