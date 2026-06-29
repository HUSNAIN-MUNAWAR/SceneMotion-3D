from pathlib import Path
from vision_core.features.pipeline_factory import load_pipeline_config, create_feature_extractor


def test_pipeline_config_loads():
    cfg = load_pipeline_config(Path('configs/pipeline/orb_fast.yaml'))
    extractor = create_feature_extractor(cfg)
    assert extractor.method in {'ORB','AKAZE','SIFT'}
