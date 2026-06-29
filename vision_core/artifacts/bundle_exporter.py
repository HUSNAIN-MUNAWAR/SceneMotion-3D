from __future__ import annotations
from pathlib import Path
import zipfile, json


def create_artifact_bundle(job_dir: str | Path, output_zip: str | Path | None = None) -> str:
    job = Path(job_dir)
    if output_zip is None:
        output_zip = job / 'artifact_bundle.zip'
    output_zip = Path(output_zip); output_zip.parent.mkdir(parents=True, exist_ok=True)
    readme = """# SceneMotion-3D Run Artifacts\n\nThis bundle contains metrics, warnings, trajectory files, point clouds, reports, selected keyframes, match visualizations, plots, and configuration where available. Monocular trajectory is relative-scale unless a valid scale reference is supplied.\n"""
    with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr('README_RUN.md', readme)
        for p in job.rglob('*'):
            if p.is_file() and p.resolve() != output_zip.resolve() and '__pycache__' not in str(p):
                zf.write(p, p.relative_to(job))
    return str(output_zip)
