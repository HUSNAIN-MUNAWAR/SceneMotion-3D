from pathlib import Path
from fastapi.testclient import TestClient
from backend.app.main import app
from scripts.generate_sample_video import main as generate
from vision_core.metrics.metrics_collector import save_metrics


def test_metrics_json_generation(tmp_path):
    metrics = save_metrics({'selected_keyframes': 1, 'average_keypoints_per_keyframe': 10, 'intrinsics_source': 'estimated'}, tmp_path/'metrics.json')
    assert (tmp_path/'metrics.json').exists()
    assert metrics['warnings']


def test_health_endpoint():
    client = TestClient(app)
    res = client.get('/health')
    assert res.status_code == 200
    assert res.json()['status'] == 'ok'


def test_job_creation_endpoint():
    generate()
    client = TestClient(app)
    res = client.post('/api/jobs/start', json={'source': 'sample', 'sample_name': 'synthetic_scene.mp4', 'config': {'max_frames': 10, 'max_keyframes': 4, 'dry_run': True}})
    assert res.status_code == 200
    assert 'job_id' in res.json()
