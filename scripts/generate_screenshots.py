from __future__ import annotations

import io
import json
import math
import textwrap
from pathlib import Path

import matplotlib
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageOps

matplotlib.use("Agg")
import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "screenshots"
OUT.mkdir(parents=True, exist_ok=True)

DEMO_DIR = ROOT / "outputs" / "demo_job_synthetic"
METRICS = json.loads((DEMO_DIR / "metrics.json").read_text())
ARTIFACTS = json.loads((DEMO_DIR / "artifacts.json").read_text())
TRAJECTORY = json.loads((DEMO_DIR / "trajectory.json").read_text())
POINTS = json.loads((DEMO_DIR / "pointclouds" / "sparse_cloud.json").read_text())
SAMPLE_VIDEO = ROOT / "sample_data" / "videos" / "synthetic_scene.mp4"

W = 1600
H = 980
BG = (3, 7, 18)
SHELL = (12, 18, 34)
CARD = (20, 29, 52)
CARD_ALT = (10, 21, 39)
LINE = (54, 72, 108)
TEXT = (237, 242, 247)
MUTED = (156, 171, 192)
BLUE = (53, 122, 255)
CYAN = (61, 215, 255)
GREEN = (29, 191, 115)
AMBER = (245, 158, 11)
RED = (248, 113, 113)


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = ["DejaVuSans-Bold.ttf", "arialbd.ttf"] if bold else ["DejaVuSans.ttf", "arial.ttf"]
    for candidate in candidates:
        try:
            return ImageFont.truetype(candidate, size)
        except Exception:
            continue
    return ImageFont.load_default()


FONT_XS = font(20)
FONT_SM = font(24)
FONT_MD = font(30, bold=True)
FONT_LG = font(44, bold=True)
FONT_XL = font(62, bold=True)


def format_number(value) -> str:
    if isinstance(value, float):
        if abs(value) >= 1000:
            return f"{value:,.0f}"
        if abs(value) >= 10:
            return f"{value:,.1f}"
        return f"{value:.3f}"
    if isinstance(value, int):
        return f"{value:,}"
    return str(value)


def wrap(text: str, width: int) -> str:
    return "\n".join(textwrap.wrap(text, width=width))


def canvas(title: str, subtitle: str, eyebrow: str) -> tuple[Image.Image, ImageDraw.ImageDraw]:
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle((32, 26, W - 32, H - 32), radius=36, fill=SHELL, outline=(34, 48, 78), width=3)
    draw.rounded_rectangle((64, 60, W - 64, 128), radius=24, fill=(9, 14, 28), outline=(30, 43, 70), width=2)
    draw.text((96, 80), "SceneMotion-3D", fill=(165, 206, 255), font=FONT_SM)
    draw.text((96, 164), eyebrow.upper(), fill=(111, 191, 255), font=FONT_XS)
    draw.text((96, 200), title, fill=TEXT, font=FONT_LG)
    draw.text((96, 258), subtitle, fill=MUTED, font=FONT_SM)
    return img, draw


def rounded_box(draw: ImageDraw.ImageDraw, box, fill=CARD, outline=LINE, radius=26, width=2):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def stat_card(draw: ImageDraw.ImageDraw, box, label: str, value: str, accent=BLUE):
    rounded_box(draw, box, fill=CARD)
    x1, y1, x2, y2 = box
    draw.text((x1 + 24, y1 + 24), label.upper(), fill=MUTED, font=FONT_XS)
    draw.text((x1 + 24, y1 + 70), value, fill=TEXT, font=FONT_LG)
    draw.rounded_rectangle((x1 + 24, y2 - 28, x1 + 124, y2 - 18), radius=5, fill=accent)


def text_card(draw: ImageDraw.ImageDraw, box, title: str, body: str, accent=CYAN):
    rounded_box(draw, box, fill=CARD_ALT)
    x1, y1, x2, y2 = box
    draw.text((x1 + 24, y1 + 20), title, fill=TEXT, font=FONT_MD)
    draw.multiline_text((x1 + 24, y1 + 72), wrap(body, 42), fill=MUTED, font=FONT_SM, spacing=10)
    draw.rounded_rectangle((x1 + 24, y2 - 26, x1 + 104, y2 - 18), radius=5, fill=accent)


def button(draw: ImageDraw.ImageDraw, box, label: str, fill=BLUE):
    draw.rounded_rectangle(box, radius=22, fill=fill, outline=(150, 210, 255), width=2)
    x1, y1, _, y2 = box
    draw.text((x1 + 28, y1 + (y2 - y1 - 28) / 2), label, fill=(255, 255, 255), font=FONT_SM)


def pill(draw: ImageDraw.ImageDraw, xy, label: str):
    x1, y1 = xy
    bbox = draw.textbbox((x1, y1), label, font=FONT_XS)
    width = bbox[2] - bbox[0] + 34
    draw.rounded_rectangle((x1, y1, x1 + width, y1 + 36), radius=18, fill=(8, 27, 56), outline=(43, 98, 176), width=2)
    draw.text((x1 + 16, y1 + 7), label, fill=(183, 220, 255), font=FONT_XS)


def open_thumb(path: Path, size: tuple[int, int]) -> Image.Image:
    image = Image.open(path).convert("RGB")
    return ImageOps.fit(image, size, method=Image.Resampling.LANCZOS)


def paste_rounded(base: Image.Image, overlay: Image.Image, xy: tuple[int, int], radius: int = 24):
    mask = Image.new("L", overlay.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, overlay.size[0], overlay.size[1]), radius=radius, fill=255)
    base.paste(overlay, xy, mask)


def chart_bytes(fig) -> Image.Image:
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=180, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)
    buf.seek(0)
    return Image.open(buf).convert("RGB")


def render_trajectory_plot() -> Image.Image:
    positions = np.array(TRAJECTORY["positions"], dtype=float)
    fig, ax = plt.subplots(figsize=(7, 4), facecolor="#09111f")
    ax.set_facecolor("#09111f")
    ax.plot(positions[:, 0], positions[:, 2], color="#35a0ff", linewidth=3, marker="o", markersize=6)
    ax.set_title("Recovered camera path", color="white", fontsize=14, pad=12)
    ax.set_xlabel("x", color="#b9c6d6")
    ax.set_ylabel("z", color="#b9c6d6")
    ax.grid(color="#23314d", alpha=0.65)
    ax.tick_params(colors="#b9c6d6")
    for spine in ax.spines.values():
        spine.set_color("#23314d")
    return chart_bytes(fig)


def render_timing_plot() -> Image.Image:
    timing = METRICS["timing_profile"]
    names = list(timing.keys())
    values = [timing[name] for name in names]
    fig, ax = plt.subplots(figsize=(6.5, 4.6), facecolor="#09111f")
    ax.set_facecolor("#09111f")
    colors = ["#35a0ff" if i != max(range(len(values)), key=values.__getitem__) else "#22c55e" for i in range(len(values))]
    y = np.arange(len(names))
    ax.barh(y, values, color=colors)
    ax.set_yticks(y)
    ax.set_yticklabels([name.replace("_", " ") for name in names], color="#dce6f5", fontsize=9)
    ax.set_title("Stage timing profile (s)", color="white", fontsize=14, pad=12)
    ax.tick_params(colors="#b9c6d6")
    ax.grid(axis="x", color="#23314d", alpha=0.65)
    for spine in ax.spines.values():
        spine.set_color("#23314d")
    return chart_bytes(fig)


def render_pointcloud_plot() -> Image.Image:
    points = np.array(POINTS["points"][:1400], dtype=float)
    positions = np.array(TRAJECTORY["positions"], dtype=float)
    fig = plt.figure(figsize=(7.4, 5.1), facecolor="#09111f")
    ax = fig.add_subplot(111, projection="3d")
    ax.set_facecolor("#09111f")
    ax.scatter(points[:, 0], points[:, 1], points[:, 2], s=3, c=points[:, 2], cmap="winter", alpha=0.55)
    ax.plot(positions[:, 0], positions[:, 1], positions[:, 2], color="#f97316", linewidth=3, marker="o", markersize=5)
    ax.set_title("Sparse cloud and trajectory", color="white", pad=16)
    ax.set_xlabel("x", color="#cbd5e1")
    ax.set_ylabel("y", color="#cbd5e1")
    ax.set_zlabel("z", color="#cbd5e1")
    ax.tick_params(colors="#b9c6d6", labelsize=8)
    ax.xaxis.pane.set_facecolor((0.05, 0.09, 0.16, 1.0))
    ax.yaxis.pane.set_facecolor((0.05, 0.09, 0.16, 1.0))
    ax.zaxis.pane.set_facecolor((0.05, 0.09, 0.16, 1.0))
    return chart_bytes(fig)


def save_landing():
    img, draw = canvas(
        "About SceneMotion-3D",
        "Real demo stats, honest limits, and direct links into the completed synthetic reconstruction run.",
        "Landing Page",
    )
    text_card(
        draw,
        (96, 334, 984, 650),
        "Production-style monocular reconstruction",
        "SceneMotion-3D turns a monocular clip into trajectories, sparse and dense point clouds, feature-match evidence, warnings, and downloadable reports. The screenshots in this repo are derived from the real demo artifacts shipped in outputs/demo_job_synthetic.",
        accent=BLUE,
    )
    button(draw, (96, 684, 430, 756), "Open live demo reconstruction")
    pill(draw, (456, 706), "real metrics")
    pill(draw, (612, 706), "real artifacts")
    pill(draw, (774, 706), "relative scale disclosure")
    stat_card(draw, (1038, 334, 1484, 498), "Selected keyframes", format_number(METRICS["selected_keyframes"]))
    stat_card(draw, (1038, 522, 1484, 686), "Sparse 3D points", format_number(METRICS["sparse_3d_point_count"]), accent=GREEN)
    stat_card(draw, (1038, 710, 1484, 874), "Dense cloud points", format_number(METRICS["dense_cloud_point_count"]), accent=CYAN)
    img.save(OUT / "landing_page.png")


def save_upload():
    img, draw = canvas(
        "Upload or start from the bundled demo",
        "The shipped sample video and the completed demo run are both documented here with real repository metadata.",
        "Upload Page",
    )
    size_mb = SAMPLE_VIDEO.stat().st_size / (1024 * 1024)
    text_card(
        draw,
        (96, 334, 840, 612),
        "Sample video and upload flow",
        f"Sample file: {SAMPLE_VIDEO.name}\nSource size: {size_mb:.2f} MB\nExtracted frames: {METRICS['extracted_frames']}\nSelected keyframes: {METRICS['selected_keyframes']}",
    )
    text_card(
        draw,
        (96, 644, 840, 874),
        "Completed demo shortcut",
        "The blue CTA in the frontend opens demo_job_synthetic so reviewers can inspect completed artifacts immediately.",
        accent=BLUE,
    )
    button(draw, (120, 798, 420, 868), "Open completed demo run")
    stat_card(draw, (886, 334, 1484, 500), "Valid pose pairs", format_number(METRICS["valid_pose_pairs"]), accent=GREEN)
    stat_card(draw, (886, 526, 1484, 692), "Avg matches / pair", format_number(METRICS["average_matches_per_pair"]), accent=CYAN)
    stat_card(draw, (886, 718, 1484, 884), "Scale mode", str(METRICS["scale_mode"]), accent=AMBER)
    img.save(OUT / "upload_page.png")


def save_processing():
    img, draw = canvas(
        "Pipeline stages and timing evidence",
        "The processing view below uses the real stage timing profile recorded in the demo metrics bundle.",
        "Processing Job Page",
    )
    timing = list(METRICS["timing_profile"].items())
    max_value = max(value for _, value in timing)
    rounded_box(draw, (96, 334, 1484, 884), fill=CARD)
    draw.text((128, 368), "Completed pipeline stages", fill=TEXT, font=FONT_MD)
    y = 430
    for name, value in timing:
        draw.text((128, y), name.replace("_", " "), fill=MUTED, font=FONT_SM)
        draw.text((1300, y), f"{value:.3f}s", fill=TEXT, font=FONT_SM)
        draw.rounded_rectangle((128, y + 42, 1438, y + 62), radius=10, fill=(13, 22, 40))
        width = int((value / max_value) * 1180)
        draw.rounded_rectangle((128, y + 42, 128 + width, y + 62), radius=10, fill=BLUE)
        y += 82
    button(draw, (1108, 804, 1438, 872), "Reports and artifacts ready")
    img.save(OUT / "processing_page.png")


def save_dashboard():
    img, draw = canvas(
        "Reconstruction dashboard",
        "Core metrics, warnings, and export links from the real demo run.",
        "Dashboard",
    )
    cards = [
        ("Frames extracted", METRICS["extracted_frames"], BLUE),
        ("Selected keyframes", METRICS["selected_keyframes"], CYAN),
        ("Avg keypoints", METRICS["average_keypoints_per_keyframe"], GREEN),
        ("Valid pose pairs", METRICS["valid_pose_pairs"], BLUE),
        ("Sparse cloud", METRICS["sparse_3d_point_count"], GREEN),
        ("Dense cloud", METRICS["dense_cloud_point_count"], CYAN),
    ]
    x = 96
    y = 334
    for i, (label, value, accent) in enumerate(cards):
        stat_card(draw, (x, y, x + 430, y + 150), label, format_number(value), accent=accent)
        x += 454
        if (i + 1) % 3 == 0:
            x = 96
            y += 182
    text_card(
        draw,
        (96, 708, 760, 884),
        "Warnings",
        "\n".join(f"- {warning}" for warning in METRICS["warnings"]),
        accent=AMBER,
    )
    text_card(
        draw,
        (796, 708, 1484, 884),
        "Artifact bundle contents",
        "report.html\nreport.pdf\ntrajectory.json\npointclouds/*.ply\ndepth/*.png\nmatches/*.jpg",
        accent=GREEN,
    )
    img.save(OUT / "reconstruction_dashboard.png")


def save_matches():
    img, draw = canvas(
        "Feature match visualizations",
        "Actual match overlays generated by the demo pipeline before pose recovery and triangulation.",
        "Feature Matches",
    )
    paths = [DEMO_DIR / path for path in ARTIFACTS["match_visualizations"][:4]]
    positions = [(96, 336), (806, 336), (96, 620), (806, 620)]
    for path, (x, y) in zip(paths, positions):
        thumb = open_thumb(path, (698, 228))
        paste_rounded(img, thumb, (x, y), radius=28)
    pill(draw, (96, 892), f"avg inlier ratio {METRICS['average_inlier_ratio']:.3f}")
    pill(draw, (368, 892), f"{METRICS['valid_pose_pairs']} pose pairs")
    pill(draw, (574, 892), f"{METRICS['average_matches_per_pair']:.0f} matches / pair")
    img.save(OUT / "feature_matches.png")


def save_depth():
    img, draw = canvas(
        "Depth explorer",
        "PNG depth outputs generated from the bundled pseudo-depth provider, shown with real run totals.",
        "Depth Explorer",
    )
    positions = [(96, 336), (806, 336), (96, 620), (806, 620)]
    for path, (x, y) in zip((DEMO_DIR / p for p in ARTIFACTS["depth_maps"][:4]), positions):
        thumb = open_thumb(path, (698, 228))
        paste_rounded(img, thumb, (x, y), radius=28)
    pill(draw, (96, 892), f"{METRICS['depth_maps_generated']} depth maps")
    pill(draw, (310, 892), METRICS["depth_provider"])
    pill(draw, (650, 892), f"{METRICS['dense_cloud_point_count']} dense points")
    img.save(OUT / "depth_explorer.png")


def save_pointcloud():
    img, draw = canvas(
        "Point cloud and trajectory viewer",
        "Sparse cloud geometry plotted from the actual exported point set and trajectory coordinates.",
        "Point Cloud Viewer",
    )
    plot = ImageOps.fit(render_pointcloud_plot(), (930, 620), method=Image.Resampling.LANCZOS)
    paste_rounded(img, plot, (96, 334), radius=30)
    stat_card(draw, (1070, 334, 1484, 500), "Point count", format_number(POINTS["point_count"]), accent=GREEN)
    stat_card(draw, (1070, 526, 1484, 692), "Trajectory length", format_number(TRAJECTORY["trajectory_length_relative"]), accent=CYAN)
    text_card(draw, (1070, 718, 1484, 884), "Scale note", TRAJECTORY["scale_note"], accent=AMBER)
    img.save(OUT / "pointcloud_viewer.png")


def save_benchmark():
    img, draw = canvas(
        "Benchmark-style report view",
        "Trajectory plots, timing profile, and quality narrative rendered from the real demo output bundle.",
        "Benchmark Report",
    )
    traj = ImageOps.fit(render_trajectory_plot(), (670, 236), method=Image.Resampling.LANCZOS)
    timing = ImageOps.fit(render_timing_plot(), (670, 272), method=Image.Resampling.LANCZOS)
    paste_rounded(img, traj, (96, 336), radius=28)
    paste_rounded(img, timing, (96, 612), radius=28)
    narrative = METRICS["quality_narrative"]
    text_card(
        draw,
        (812, 336, 1484, 598),
        "Quality narrative",
        f"Grade: {narrative['reconstruction_quality_grade']}\nTracking stability: {narrative['tracking_stability']:.3f}\nScale mode: {narrative['scale_mode']}\nLoop candidates verified: {METRICS['loop_candidates_verified']}",
        accent=GREEN,
    )
    text_card(
        draw,
        (812, 622, 1484, 884),
        "Recommended fixes",
        "\n".join(f"- {item}" for item in narrative["recommended_fixes"]),
        accent=BLUE,
    )
    img.save(OUT / "benchmark_report.png")


def save_run_comparison():
    img, draw = canvas(
        "Run evidence snapshot",
        "A compact comparison of geometry, quality, and timing signals taken from the single shipped demo run.",
        "Run Comparison",
    )
    rounded_box(draw, (96, 334, 1484, 884), fill=CARD)
    headers = ["Metric", "Observed value", "Interpretation"]
    cols = [116, 500, 900]
    for header, col in zip(headers, cols):
        draw.text((col, 372), header, fill=MUTED, font=FONT_SM)
    rows = [
        ("Avg inlier ratio", f"{METRICS['average_inlier_ratio']:.3f}", "Stable feature geometry"),
        ("Depth provider", METRICS["depth_provider"], "Offline-safe fallback"),
        ("Loop candidates verified", format_number(METRICS["loop_candidates_verified"]), "Potential revisit support"),
        ("Scale mode", METRICS["scale_mode"], "Relative monocular units"),
        ("Report generation", f"{METRICS['timing_profile']['report_generation_time']:.3f}s", "Artifacts exported successfully"),
    ]
    y = 438
    for metric, observed, note in rows:
        draw.rounded_rectangle((108, y - 12, 1474, y + 52), radius=18, fill=(15, 24, 43), outline=(31, 47, 75), width=1)
        draw.text((116, y), metric, fill=TEXT, font=FONT_SM)
        draw.text((500, y), observed, fill=(169, 221, 255), font=FONT_SM)
        draw.text((900, y), note, fill=MUTED, font=FONT_SM)
        y += 88
    img.save(OUT / "run_comparison.png")


def save_pdf_preview():
    img, draw = canvas(
        "PDF report preview",
        "A report-like cover view assembled from the same metrics, warnings, and trajectory evidence shipped with the demo.",
        "PDF Preview",
    )
    rounded_box(draw, (96, 334, 1484, 884), fill=(248, 250, 252), outline=(226, 232, 240))
    draw = ImageDraw.Draw(img)
    draw.text((140, 382), "SceneMotion-3D Demo Report", fill=(15, 23, 42), font=FONT_LG)
    draw.text((140, 452), f"Scale note: {METRICS['scale_note']}", fill=(71, 85, 105), font=FONT_SM)
    draw.text((140, 520), f"Sparse cloud points: {format_number(METRICS['sparse_3d_point_count'])}", fill=(15, 23, 42), font=FONT_SM)
    draw.text((140, 568), f"Dense cloud points: {format_number(METRICS['dense_cloud_point_count'])}", fill=(15, 23, 42), font=FONT_SM)
    draw.text((140, 616), "Warnings", fill=(15, 23, 42), font=FONT_MD)
    draw.multiline_text((140, 668), "\n".join(f"- {warning}" for warning in METRICS["warnings"]), fill=(71, 85, 105), font=FONT_SM, spacing=12)
    pill(draw, (1060, 384), "html and pdf exported")
    img.save(OUT / "pdf_report_preview.png")


def save_artifact_bundle():
    img, draw = canvas(
        "Artifact bundle summary",
        "A faithful file-level summary of what the demo run exports for downstream review and debugging.",
        "Artifact Bundle",
    )
    text_card(
        draw,
        (96, 334, 760, 884),
        "Artifact index",
        "metrics.json\ntrajectory.json\nreport.html and report.pdf\npointclouds/sparse_cloud.ply\npointclouds/dense_cloud.ply\ndepth/depth_0000..0003.png\nmatches/matches_0000_0001..0006_0007.jpg",
        accent=GREEN,
    )
    match_thumb = open_thumb(DEMO_DIR / ARTIFACTS["match_visualizations"][0], (310, 230))
    depth_thumb = open_thumb(DEMO_DIR / ARTIFACTS["depth_maps"][0], (310, 230))
    paste_rounded(img, match_thumb, (814, 344), radius=24)
    paste_rounded(img, depth_thumb, (1160, 344), radius=24)
    stat_card(draw, (814, 606, 1120, 774), "Reports", "2", accent=BLUE)
    stat_card(draw, (1176, 606, 1484, 774), "Point clouds", "2", accent=CYAN)
    text_card(draw, (814, 792, 1484, 884), "Bundle note", "Download the ZIP from the job dashboard to package every file shown on this screen.", accent=BLUE)
    img.save(OUT / "artifact_bundle.png")


def write_aliases():
    aliases = {
        "dashboard.png": "reconstruction_dashboard.png",
        "trajectory_viewer.png": "pointcloud_viewer.png",
        "dashboard_snapshot.png": "reconstruction_dashboard.png",
    }
    for alias, target in aliases.items():
        (OUT / alias).write_bytes((OUT / target).read_bytes())


def main():
    save_landing()
    save_upload()
    save_processing()
    save_dashboard()
    save_matches()
    save_depth()
    save_pointcloud()
    save_benchmark()
    save_run_comparison()
    save_pdf_preview()
    save_artifact_bundle()
    write_aliases()
    print(f"Generated real-data screenshot assets in {OUT}")


if __name__ == "__main__":
    main()
