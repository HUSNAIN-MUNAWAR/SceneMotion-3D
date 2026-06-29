import numpy as np
from vision_core.reconstruction.cloud_filters import voxel_downsample, remove_statistical_outliers, normalize_for_viewer


def test_cloud_filters():
    pts = np.array([[0,0,0],[0.01,0,0],[1,1,1],[100,100,100]], dtype=float)
    assert len(voxel_downsample(pts, 0.05)) <= len(pts)
    assert normalize_for_viewer(remove_statistical_outliers(pts)).shape[1] == 3
