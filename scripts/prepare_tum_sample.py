from pathlib import Path
import argparse, json, sys
ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT))
from vision_core.datasets.tum_rgbd import prepare_tum_dataset
p = argparse.ArgumentParser(); p.add_argument('dataset_path'); p.add_argument('--out', default='outputs/tum_dataset')
args = p.parse_args(); print(json.dumps(prepare_tum_dataset(args.dataset_path, ROOT/args.out), indent=2))
