from __future__ import annotations
from pathlib import Path
import json
from dataclasses import dataclass, asdict

@dataclass
class DatasetMetadata:
    dataset_type: str
    source_path: str
    frames_path: str | None
    trajectory_path: str | None
    frame_count: int
    warnings: list[str]

    def save(self, output_path: str | Path) -> str:
        p = Path(output_path); p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(asdict(self), indent=2), encoding='utf-8')
        return str(p)


def require_path(path: str | Path, label: str) -> Path:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f'{label} not found: {p}')
    return p
