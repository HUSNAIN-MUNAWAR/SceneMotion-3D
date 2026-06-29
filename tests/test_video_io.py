from pathlib import Path
from scripts.generate_sample_video import main as generate
from vision_core.io.video_reader import read_video_metadata
from vision_core.io.frame_extractor import extract_frames


def test_video_metadata_and_frame_extraction(tmp_path):
    generate()
    video = Path('sample_data/videos/synthetic_scene.mp4')
    meta = read_video_metadata(video)
    assert meta.frame_count > 0
    out = tmp_path / 'frames'
    result = extract_frames(video, out, target_fps=3, max_frames=10)
    assert result['selected_frame_count'] > 0
    assert len(list(out.glob('*.jpg'))) == result['selected_frame_count']
