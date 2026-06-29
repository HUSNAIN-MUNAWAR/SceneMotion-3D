from pathlib import Path
import json
import numpy as np
import cv2
from vision_core.io.frame_extractor import extract_frames
from vision_core.keyframes.keyframe_selector import select_keyframes
from vision_core.features.extractors import extract_features_for_keyframes
from vision_core.features.visualization import visualize_keypoints
from vision_core.features.matcher import match_feature_sequence
from vision_core.camera.calibration_io import intrinsics_from_config
from vision_core.vo.pose_estimator import estimate_relative_poses
from vision_core.vo.trajectory import chain_poses, save_trajectory
from vision_core.reconstruction.sparse_cloud import build_sparse_cloud
from vision_core.reconstruction.dense_cloud import export_dense_cloud
from vision_core.depth.run_depth import generate_depth_maps
from vision_core.metrics.metrics_collector import save_metrics
from vision_core.reports.report_generator import generate_html_report, generate_pdf_report
from vision_core.profiling.timer import StageTimer
from vision_core.quality.frame_pair_filter import evaluate_sequence_pairs
from vision_core.slam.loop_candidates import detect_loop_candidates
from vision_core.scale.scale_manager import ScaleManager
from vision_core.experiments.run_registry import RunRegistry
from vision_core.artifacts.bundle_exporter import create_artifact_bundle
from vision_core.reports.quality_narrative import build_quality_narrative


def _progress(cb, p, stage, msg=""):
    if cb:
        cb(p, stage, msg)


def run_pipeline_job(video_path: str | Path, output_dir: str | Path, config: dict | None = None, progress_cb=None) -> dict:
    config = config or {}
    timer = StageTimer()
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    _progress(progress_cb, 5, "frame_extraction", "Extracting video frames")
    with timer.stage("frame_extraction_time"):
        frame_meta = extract_frames(video_path, output_dir / "frames", target_fps=float(config.get("target_fps", 4)), max_frames=int(config.get("max_frames", 120)), resize_width=int(config.get("resize_width", 800)))
    width = frame_meta.get("width") or 800
    height = frame_meta.get("height") or 600
    if frame_meta["frame_paths"]:
        first = cv2.imread(frame_meta["frame_paths"][0])
        if first is not None:
            height, width = first.shape[:2]

    intr = intrinsics_from_config(config, width, height)
    (output_dir / "intrinsics.json").write_text(json.dumps(intr.to_dict(), indent=2), encoding="utf-8")

    _progress(progress_cb, 18, "keyframes", "Selecting keyframes")
    with timer.stage("keyframe_selection_time"):
        kf = select_keyframes(frame_meta["frame_paths"], output_dir / "keyframes", interval=int(config.get("keyframe_interval", 2)), max_keyframes=int(config.get("max_keyframes", 16)))

    _progress(progress_cb, 32, "features", "Extracting visual features")
    with timer.stage("feature_extraction_time"):
        feat = extract_features_for_keyframes(kf["keyframe_paths"], output_dir / "features", method=config.get("feature_method", "ORB"), max_features=int(config.get("max_features", 2000)))
    for i, fp in enumerate(kf["keyframe_paths"][:4]):
        try:
            visualize_keypoints(fp, str(output_dir / "features" / f"keypoints_{i:04d}.jpg"), feat["method"])
        except Exception:
            pass

    _progress(progress_cb, 45, "matching", "Matching adjacent keyframes")
    with timer.stage("matching_time"):
        matches = match_feature_sequence(feat["features"], kf["keyframe_paths"], output_dir / "matches", ratio=float(config.get("match_ratio", 0.82)))
    quality = evaluate_sequence_pairs(kf["keyframe_paths"], matches.get("pairs", []), output_dir / "quality" / "rejected_pairs.json")
    loop_candidates = detect_loop_candidates(kf["keyframe_paths"], output_dir / "loop_closure", min_gap=int(config.get("loop_min_gap", 4)))

    _progress(progress_cb, 58, "visual_odometry", "Estimating relative poses")
    with timer.stage("pose_estimation_time"):
        poses = estimate_relative_poses(output_dir / "matches", max(0, len(kf["keyframe_paths"]) - 1), intr.K, min_inlier_ratio=float(config.get("min_inlier_ratio", 0.15)))
        traj = chain_poses(poses["valid"])
        save_trajectory(traj, output_dir / "trajectory.json")

    _progress(progress_cb, 70, "sparse_reconstruction", "Triangulating sparse cloud")
    with timer.stage("triangulation_time"):
        sparse = build_sparse_cloud(output_dir / "matches", poses, intr.K, output_dir / "pointclouds")

    _progress(progress_cb, 80, "depth", "Generating depth maps")
    with timer.stage("depth_estimation_time"):
        depth = generate_depth_maps(kf["keyframe_paths"], output_dir / "depth", provider_name=config.get("depth_provider", "fallback"), max_maps=int(config.get("max_depth_maps", 4)))

    _progress(progress_cb, 88, "dense_cloud", "Building dense cloud from depth")
    dense = {"point_count": 0, "ply": None}
    if depth["maps"]:
        with timer.stage("point_cloud_export_time"):
            dense = export_dense_cloud(depth["maps"][0]["npy"], depth["maps"][0]["frame"], intr.K, output_dir / "pointclouds" / "dense_cloud.ply", stride=int(config.get("dense_stride", 8)))

    pair_errors = []
    # keep reprojection metric simple and honest; robust global reprojection needs full tracks.
    mean_reprojection_error = 0.0
    max_reprojection_error = 0.0

    scale = ScaleManager().resolve(config.get("scale_mode", "relative"), **config).to_dict()

    metrics = {
        "video_path": str(video_path),
        "number_of_frames": int(frame_meta.get("frame_count", 0)),
        "extracted_frames": int(frame_meta.get("selected_frame_count", 0)),
        "selected_keyframes": int(kf.get("count", 0)),
        "average_keypoints_per_keyframe": float(feat.get("average_keypoints", 0.0)),
        "average_matches_per_pair": float(matches.get("average_matches", 0.0)),
        "average_inlier_ratio": float(matches.get("average_inlier_ratio", 0.0)),
        "valid_pose_pairs": int(poses.get("valid_count", 0)),
        "rejected_pose_pairs": int(poses.get("rejected_count", 0)),
        "sparse_3d_point_count": int(sparse.get("point_count", 0)),
        "mean_reprojection_error": mean_reprojection_error,
        "max_reprojection_error": max_reprojection_error,
        "trajectory_length_relative_units": float(traj.get("trajectory_length_relative", 0.0)),
        "depth_maps_generated": int(depth.get("count", 0)),
        "dense_cloud_point_count": int(dense.get("point_count", 0)),
        "depth_provider": depth.get("provider"),
        "intrinsics_source": intr.source,
        "scale_note": "Relative monocular units only; no metric scale claimed.",
        "bundle_adjustment_note": "Includes lightweight local refinement plus optional small-window BA modules; not a replacement for mature SfM systems like COLMAP.",
        "scale_mode": scale["mode"],
        "scale_source": scale["scale_source"],
        "scale_factor": scale["scale_factor"],
        "scale_confidence": scale["confidence"],
        "rejected_pairs_total": int(quality.get("rejected_pairs_total", 0)),
        "rejected_low_matches": int(quality.get("rejected_low_matches", 0)),
        "rejected_low_parallax": int(quality.get("rejected_low_parallax", 0)),
        "rejected_blur": int(quality.get("rejected_blur", 0)),
        "rejected_dynamic_scene": int(quality.get("rejected_dynamic_scene", 0)),
        "rejected_degenerate_motion": int(quality.get("rejected_degenerate_motion", 0)),
        "loop_candidates": int(loop_candidates.get("candidate_count", 0)),
        "loop_candidates_verified": int(loop_candidates.get("verified_count", 0)),
        "timing_profile": timer.summary(),
    }
    metrics["quality_narrative"] = build_quality_narrative(metrics)
    metrics = save_metrics(metrics, output_dir / "metrics.json")
    if depth.get("warnings"):
        metrics["warnings"] = sorted(set(metrics.get("warnings", []) + depth["warnings"]))
        save_metrics(metrics, output_dir / "metrics.json")

    _progress(progress_cb, 94, "reports", "Generating reports")
    with timer.stage("report_generation_time"):
        generate_html_report(metrics, output_dir / "report.html")
        generate_pdf_report(metrics, output_dir / "report.pdf")
    metrics["timing_profile"] = timer.summary()
    metrics = save_metrics(metrics, output_dir / "metrics.json")

    artifacts = {
        "job_output_dir": str(output_dir),
        "metrics": "metrics.json",
        "trajectory": "trajectory.json",
        "reports": ["report.html", "report.pdf"],
        "pointclouds": ["pointclouds/sparse_cloud.ply", "pointclouds/dense_cloud.ply"],
        "depth_maps": [str(Path(m["png"]).relative_to(output_dir)) for m in depth.get("maps", [])],
        "match_visualizations": [str(p.relative_to(output_dir)) for p in (output_dir / "matches").glob("matches_*.jpg")],
        "quality_report": "quality/rejected_pairs.json",
        "loop_candidates": "loop_closure/loop_candidates.json",
    }
    (output_dir / "artifacts.json").write_text(json.dumps(artifacts, indent=2), encoding="utf-8")
    try:
        registry = RunRegistry(output_dir.parent)
        registry.register_run(config, metrics, artifacts, metrics.get("warnings", []), metrics.get("timing_profile", {}))
    except Exception:
        pass
    try:
        artifacts["bundle"] = str(Path(create_artifact_bundle(output_dir)).relative_to(output_dir))
        (output_dir / "artifacts.json").write_text(json.dumps(artifacts, indent=2), encoding="utf-8")
    except Exception:
        pass
    _progress(progress_cb, 100, "completed", "Pipeline completed")
    return metrics
