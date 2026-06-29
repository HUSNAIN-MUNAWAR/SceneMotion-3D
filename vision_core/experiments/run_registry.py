from __future__ import annotations
from pathlib import Path
import json, time, uuid

class RunRegistry:
    def __init__(self, root: str | Path):
        self.root = Path(root); self.root.mkdir(parents=True, exist_ok=True)
        self.index_path = self.root / 'runs_index.json'
        if not self.index_path.exists(): self.index_path.write_text('[]', encoding='utf-8')

    def list_runs(self) -> list[dict]:
        return json.loads(self.index_path.read_text(encoding='utf-8'))

    def register_run(self, config: dict, metrics: dict, artifacts: dict, warnings: list[str] | None = None, timing_profile: dict | None = None) -> dict:
        run = {"run_id": f"run_{uuid.uuid4().hex[:10]}", "created_at": time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()), "config": config, "metrics": metrics, "warnings": warnings or metrics.get('warnings', []), "artifacts": artifacts, "timing_profile": timing_profile or metrics.get('timing_profile', {}), "quality_score": self.quality_score(metrics)}
        runs = self.list_runs(); runs.append(run); self.index_path.write_text(json.dumps(runs, indent=2), encoding='utf-8')
        return run

    @staticmethod
    def quality_score(metrics: dict) -> float:
        score = 100.0
        score -= max(0, 120 - metrics.get('average_keypoints_per_keyframe', 0)) * 0.12
        score -= max(0, 30 - metrics.get('average_matches_per_pair', 0)) * 0.5
        score -= max(0, 0.35 - metrics.get('average_inlier_ratio', 0)) * 60
        score -= min(30, len(metrics.get('warnings', [])) * 5)
        return float(max(0, min(100, score)))

    def compare(self, run_id_a: str, run_id_b: str) -> dict:
        runs = {r['run_id']: r for r in self.list_runs()}
        a, b = runs[run_id_a], runs[run_id_b]
        keys = sorted(set(a.get('metrics',{})) & set(b.get('metrics',{})))
        deltas = {}
        for k in keys:
            if isinstance(a['metrics'].get(k), (int,float)) and isinstance(b['metrics'].get(k), (int,float)):
                deltas[k] = b['metrics'][k] - a['metrics'][k]
        return {"a": run_id_a, "b": run_id_b, "quality_delta": b.get('quality_score',0)-a.get('quality_score',0), "metric_deltas": deltas}
