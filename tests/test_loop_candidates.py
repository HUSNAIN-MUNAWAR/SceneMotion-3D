import cv2, numpy as np
from vision_core.slam.loop_candidates import detect_loop_candidates


def test_loop_candidate_json(tmp_path):
    paths=[]
    for i in range(6):
        img = np.zeros((120,160,3), dtype=np.uint8)
        cv2.circle(img, (50+i%2*5,60), 25, (255,255,255), -1)
        p = tmp_path / f'{i}.jpg'; cv2.imwrite(str(p), img); paths.append(str(p))
    out = detect_loop_candidates(paths, tmp_path/'loops', min_gap=2, similarity_threshold=0.1)
    assert 'candidate_count' in out
    assert (tmp_path/'loops'/'loop_candidates.json').exists()
