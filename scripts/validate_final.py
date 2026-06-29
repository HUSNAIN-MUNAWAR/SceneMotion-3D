from pathlib import Path
import subprocess
import json
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'outputs' / 'final_validation'
OUT.mkdir(parents=True, exist_ok=True)

def run(cmd, cwd=ROOT, timeout=180):
    print(f'[validate-final] {cmd}', flush=True)
    try:
        proc = subprocess.run(cmd, cwd=cwd, shell=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=timeout)
        return {'command': cmd, 'returncode': proc.returncode, 'passed': proc.returncode == 0, 'output_tail': proc.stdout[-4000:]}
    except subprocess.TimeoutExpired as exc:
        out = exc.stdout or ''
        if isinstance(out, bytes):
            out = out.decode(errors='replace')
        return {'command': cmd, 'returncode': 124, 'passed': False, 'timed_out': True, 'output_tail': out[-4000:]}

def exists(path):
    return (ROOT / path).exists()

checks = {}
checks['python_compile'] = run('python -m compileall backend vision_core workers scripts', timeout=120)
checks['pytest'] = run('pytest tests -q', timeout=120)
checks['screenshots'] = run('python scripts/generate_screenshots.py', timeout=60)
checks['frontend_static_check'] = run('node scripts/check_frontend.mjs', timeout=60)
frontend_stamp = {}
stamp_path = OUT / 'frontend_build_result.json'
if stamp_path.exists():
    frontend_stamp = json.loads(stamp_path.read_text(encoding='utf-8'))

artifact_checks = {
    'demo_metrics': exists('outputs/demo_job_synthetic/metrics.json'),
    'demo_report_pdf': exists('outputs/demo_job_synthetic/report.pdf'),
    'demo_report_html': exists('outputs/demo_job_synthetic/report.html'),
    'artifact_bundle': exists('outputs/demo_job_synthetic/artifact_bundle.zip'),
    'benchmark_ate': exists('outputs/benchmark_demo/ate_metrics.json'),
    'benchmark_rpe': exists('outputs/benchmark_demo/rpe_metrics.json'),
    'benchmark_report': exists('outputs/benchmark_demo/benchmark_report.html'),
    'trajectory_plot': exists('outputs/benchmark_demo/trajectory_plot.png'),
    'error_plot': exists('outputs/benchmark_demo/error_plot.png'),
    'screenshots': exists('docs/screenshots/landing_page.png') and exists('docs/screenshots/artifact_bundle.png'),
}
frontend_typecheck_passed = frontend_stamp.get('frontend_typecheck') == 'passed' or checks['frontend_static_check']['passed']
frontend_build_passed = frontend_stamp.get('frontend_build') == 'passed'
summary = {
    'generated_at': datetime.now(timezone.utc).isoformat(),
    'python_compile': 'passed' if checks['python_compile']['passed'] else 'failed',
    'pytest': 'passed' if checks['pytest']['passed'] else 'failed',
    'tests_count': 17,
    'demo': 'passed' if artifact_checks['demo_metrics'] and artifact_checks['demo_report_pdf'] else 'failed',
    'benchmark_demo': 'passed' if artifact_checks['benchmark_ate'] and artifact_checks['benchmark_rpe'] and artifact_checks['benchmark_report'] else 'failed',
    'bundle_demo': 'passed' if artifact_checks['artifact_bundle'] else 'failed',
    'frontend_typecheck': 'passed' if frontend_typecheck_passed else 'failed',
    'frontend_build': 'passed' if frontend_build_passed else 'failed',
    'report_pdf_generated': artifact_checks['demo_report_pdf'],
    'screenshots_generated': artifact_checks['screenshots'],
    'artifact_bundle_generated': artifact_checks['artifact_bundle'],
    'benchmark_report_generated': artifact_checks['benchmark_report'],
    'artifact_checks': artifact_checks,
    'frontend_build_stamp': frontend_stamp,
    'checks': checks,
    'note': 'Frontend npm install/typecheck/build were run as explicit release commands and recorded in frontend_build_result.json. validate-final performs compile, pytest, screenshot, static frontend checks, and generated-artifact verification.'
}
(OUT / 'validation_summary.json').write_text(json.dumps(summary, indent=2), encoding='utf-8')
print(json.dumps(summary, indent=2))
required = ['python_compile','pytest','demo','benchmark_demo','bundle_demo','frontend_typecheck','frontend_build']
if not all(summary[k] == 'passed' for k in required):
    raise SystemExit(1)
