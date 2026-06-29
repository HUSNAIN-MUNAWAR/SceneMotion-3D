from pathlib import Path
import argparse, json, sys
ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT))
from vision_core.datasets.euroc import prepare_euroc_dataset
p = argparse.ArgumentParser(); p.add_argument('dataset_path'); p.add_argument('--out', default='outputs/euroc_dataset')
args = p.parse_args(); print(json.dumps(prepare_euroc_dataset(args.dataset_path, ROOT/args.out), indent=2))
