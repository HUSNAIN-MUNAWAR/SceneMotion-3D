from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from vision_core.experiments.run_registry import RunRegistry
from backend.app.core.config import get_settings

router = APIRouter(prefix='/api/experiments', tags=['experiments'])
registry = RunRegistry(get_settings().output_dir)

class CompareRequest(BaseModel):
    run_id_a: str
    run_id_b: str

@router.get('')
def list_experiments():
    return registry.list_runs()

@router.get('/{run_id}')
def get_experiment(run_id: str):
    for run in registry.list_runs():
        if run.get('run_id') == run_id:
            return run
    raise HTTPException(status_code=404, detail='Run not found')

@router.post('/compare')
def compare_runs(req: CompareRequest):
    try:
        return registry.compare(req.run_id_a, req.run_id_b)
    except KeyError:
        raise HTTPException(status_code=404, detail='One or both run IDs were not found')
