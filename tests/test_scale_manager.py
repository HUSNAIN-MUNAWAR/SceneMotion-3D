from vision_core.scale.scale_manager import ScaleManager


def test_relative_scale_warning():
    r = ScaleManager().resolve('relative').to_dict()
    assert r['scale_factor'] == 1.0
    assert 'Relative scale only' in ' '.join(r['warnings'])

def test_known_distance_scale():
    r = ScaleManager().resolve('known_distance', observed_relative_distance=2, known_metric_distance=10).to_dict()
    assert r['scale_factor'] == 5
    assert r['confidence'] > 0
