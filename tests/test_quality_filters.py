import cv2, numpy as np
from vision_core.quality.blur import is_blurry
from vision_core.quality.frame_pair_filter import evaluate_frame_pair


def test_quality_filter_returns_reasons(tmp_path):
    img = np.zeros((100,100,3), dtype=np.uint8)
    p1 = tmp_path/'a.jpg'; p2 = tmp_path/'b.jpg'
    cv2.imwrite(str(p1), img); cv2.imwrite(str(p2), img)
    assert is_blurry(str(p1))['is_blurry']
    rep = evaluate_frame_pair(str(p1), str(p2), {'filtered_matches': 0, 'inlier_ratio': 0})
    assert not rep['accepted']
    assert 'blur' in rep['reasons']
