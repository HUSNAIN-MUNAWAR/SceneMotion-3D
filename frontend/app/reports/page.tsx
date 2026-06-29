import MetricsCards from '@/components/MetricsCards';
export default function ReportsPage() {
  const metrics = { selected_keyframes: 0, average_keypoints_per_keyframe: 0, average_matches_per_pair: 0, average_inlier_ratio: 0, valid_pose_pairs: 0, sparse_3d_point_count: 0, dense_cloud_point_count: 0, trajectory_length_relative_units: 0 };
  return <main className="min-h-screen p-8"><div className="mx-auto max-w-5xl"><h1 className="text-3xl font-bold text-white">Metrics and Reports</h1><p className="mt-3 text-slate-400">Metrics are populated from /api/jobs/{'{job_id}'}/metrics for completed jobs.</p><div className="mt-6"><MetricsCards metrics={metrics} /></div></div></main>;
}
