from pathlib import Path
from fastapi import APIRouter
from vision_core.features.pipeline_factory import load_available_presets

router = APIRouter(prefix='/api/config', tags=['config'])

@router.get('/presets')
def presets():
    root = Path(__file__).resolve().parents[3]
    return load_available_presets(root / 'configs' / 'pipeline')
