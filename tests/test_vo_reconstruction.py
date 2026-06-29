import numpy as np
from vision_core.vo.essential_matrix import estimate_essential
from vision_core.reconstruction.triangulation import triangulate_pair
from vision_core.reconstruction.ply_exporter import export_ply


def test_essential_matrix_graceful_failure():
    K = np.eye(3)
    E, mask, status = estimate_essential(np.zeros((4,2), dtype=np.float32), np.zeros((4,2), dtype=np.float32), K)
    assert E is None
    assert status == 'too_few_matches'


def test_triangulation_and_ply(tmp_path):
    kp1 = np.array([[10,10],[20,20],[30,30]], dtype=np.float32)
    kp2 = kp1 + np.array([2,0], dtype=np.float32)
    matches = np.array([[0,0,0],[1,1,0],[2,2,0]], dtype=np.float32)
    K = np.array([[100,0,20],[0,100,20],[0,0,1]], dtype=float)
    R = np.eye(3)
    t = np.array([1,0,0], dtype=float)
    pts = triangulate_pair(kp1, kp2, matches, K, R, t)
    assert pts.shape[1] == 3
    ply = export_ply(pts, tmp_path/'cloud.ply')
    assert (tmp_path/'cloud.ply').exists()
    assert 'element vertex' in (tmp_path/'cloud.ply').read_text()
