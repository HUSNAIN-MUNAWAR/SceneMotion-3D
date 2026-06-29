export default function MetricsCards({ metrics }: { metrics: Record<string, any> }) {
  const keys = ['selected_keyframes','average_keypoints_per_keyframe','average_matches_per_pair','average_inlier_ratio','valid_pose_pairs','sparse_3d_point_count','dense_cloud_point_count','trajectory_length_relative_units'];
  return <div className="grid gap-4 md:grid-cols-4">{keys.map(k => <div key={k} className="card p-4"><p className="text-xs uppercase tracking-wide text-slate-500">{k.replaceAll('_',' ')}</p><p className="mt-2 text-2xl font-bold text-white">{Number(metrics[k] ?? 0).toFixed(typeof metrics[k] === 'number' && metrics[k] < 10 ? 2 : 0)}</p></div>)}</div>;
}
