from pathlib import Path
from scripts.generate_sample_video import main as generate
from vision_core.io.frame_extractor import extract_frames
from vision_core.keyframes.keyframe_selector import select_keyframes
from vision_core.features.extractors import extract_features_for_keyframes
from vision_core.features.matcher import match_feature_sequence


def test_keyframes_orb_and_matching(tmp_path):
    generate()
    frames = extract_frames('sample_data/videos/synthetic_scene.mp4', tmp_path/'frames', target_fps=4, max_frames=20)
    kf = select_keyframes(frames['frame_paths'], tmp_path/'keyframes', interval=1, max_keyframes=8, min_sharpness=1)
    assert kf['count'] >= 2
    feat = extract_features_for_keyframes(kf['keyframe_paths'], tmp_path/'features', method='ORB')
    assert feat['average_keypoints'] > 10
    matches = match_feature_sequence(feat['features'], kf['keyframe_paths'], tmp_path/'matches')
    assert 'average_matches' in matches
