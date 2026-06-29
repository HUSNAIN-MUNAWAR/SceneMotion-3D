from pathlib import Path
import argparse, json, sys
ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT))
from vision_core.datasets.kitti import prepare_kitti_dataset
p = argparse.ArgumentParser(); p.add_argument('sequence_path'); p.add_argument('--poses-file', default=None); p.add_argument('--out', default='outputs/kitti_dataset')
args = p.parse_args(); print(json.dumps(prepare_kitti_dataset(args.sequence_path, ROOT/args.out, args.poses_file), indent=2))
