from pathlib import Path
import html, json
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

DISCLAIMER = "SceneMotion-3D estimates relative monocular trajectory by default. Absolute metric scale requires additional information such as known camera intrinsics, known object size, known camera height, stereo baseline, depth sensor, IMU, or ground-truth alignment for evaluation. Fallback pseudo-depth is provided for offline demonstration only and must not be interpreted as metric depth."


def _val(v):
    if isinstance(v, (dict, list)):
        return json.dumps(v, indent=2)[:1600]
    return str(v)


def generate_html_report(metrics: dict, output_path: str | Path) -> str:
    output_path = Path(output_path)
    rows = "\n".join(f"<tr><th>{html.escape(str(k))}</th><td><pre>{html.escape(_val(v))}</pre></td></tr>" for k, v in metrics.items() if k != "warnings")
    warnings = "".join(f"<li>{html.escape(w)}</li>" for w in metrics.get("warnings", []))
    fixes = "".join(f"<li>{html.escape(x)}</li>" for x in metrics.get('quality_narrative', {}).get('recommended_fixes', []))
    body = f"""<!doctype html>
<html><head><meta charset='utf-8'><title>SceneMotion 3D Report</title>
<style>body{{font-family:Inter,Arial,sans-serif;margin:40px;background:#0f172a;color:#e5e7eb}}.card{{background:#111827;border:1px solid #334155;border-radius:16px;padding:24px;box-shadow:0 10px 30px #0004}}table{{border-collapse:collapse;width:100%}}th,td{{border-bottom:1px solid #334155;text-align:left;padding:10px;vertical-align:top}}th{{width:320px;color:#bfdbfe}}pre{{white-space:pre-wrap;margin:0;color:#e5e7eb}}.warn{{background:#451a03;border:1px solid #fed7aa;border-radius:12px;padding:16px}}.note{{background:#172554;border:1px solid #60a5fa;border-radius:12px;padding:16px}}</style>
</head><body><div class='card'><h1>SceneMotion 3D Reconstruction Report</h1>
<div class='note'><b>Scale disclaimer:</b> {html.escape(DISCLAIMER)}</div>
<h2>Metrics</h2><table>{rows}</table><h2>Warnings and Limitations</h2><div class='warn'><ul>{warnings}</ul></div><h2>Recommended Fixes</h2><ul>{fixes}</ul></div></body></html>"""
    output_path.write_text(body, encoding="utf-8")
    return str(output_path)


def generate_pdf_report(metrics: dict, output_path: str | Path) -> str:
    output_path = Path(output_path)
    doc = SimpleDocTemplate(str(output_path), pagesize=letter)
    styles = getSampleStyleSheet()
    story = [Paragraph("SceneMotion 3D Reconstruction Report", styles["Title"]), Spacer(1, 12)]
    story.append(Paragraph(DISCLAIMER, styles["BodyText"]))
    story.append(Spacer(1, 12))
    table_data = [[Paragraph("Metric", styles["BodyText"]), Paragraph("Value", styles["BodyText"])] ]
    for k, v in metrics.items():
        if k != "warnings":
            table_data.append([Paragraph(str(k), styles["BodyText"]), Paragraph(html.escape(_val(v)), styles["BodyText"])])
    table = Table(table_data, colWidths=[185, 335], repeatRows=1)
    table.setStyle(TableStyle([("BACKGROUND", (0,0), (-1,0), colors.lightgrey), ("GRID", (0,0), (-1,-1), 0.25, colors.grey), ("VALIGN", (0,0), (-1,-1), "TOP")]))
    story.append(table)
    story.append(Spacer(1, 12))
    story.append(Paragraph("Warnings and limitations", styles["Heading2"]))
    for w in metrics.get("warnings", []):
        story.append(Paragraph(f"- {html.escape(w)}", styles["BodyText"]))
    story.append(Paragraph("Recommended fixes", styles["Heading2"]))
    for x in metrics.get('quality_narrative', {}).get('recommended_fixes', []):
        story.append(Paragraph(f"- {html.escape(x)}", styles["BodyText"]))
    doc.build(story)
    return str(output_path)
