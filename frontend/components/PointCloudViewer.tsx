'use client';

type PointCloudMetrics = {
  sparse_3d_point_count?: number;
  dense_cloud_point_count?: number;
  depth_provider?: string;
  scale_note?: string;
};

export default function PointCloudViewer({ jobId, apiBase, metrics }: { jobId: string; apiBase: string; metrics?: PointCloudMetrics }) {
  const stats = [
    { label: 'Sparse points', value: metrics?.sparse_3d_point_count ?? 0 },
    { label: 'Dense points', value: metrics?.dense_cloud_point_count ?? 0 },
    { label: 'Depth provider', value: metrics?.depth_provider ?? 'fallback_pseudo_depth' },
  ];

  return <div className="card p-6"><h2 className="font-semibold text-white">3D point cloud outputs</h2><p className="mt-2 text-sm text-slate-400">This demo exposes the real sparse and dense clouds produced by the bundled synthetic reconstruction run.</p><div className="mt-5 grid gap-3 md:grid-cols-3">{stats.map(stat => <div key={stat.label} className="rounded-2xl border border-slate-700 bg-slate-950/60 p-4"><p className="text-xs uppercase tracking-[0.24em] text-slate-500">{stat.label}</p><p className="mt-2 text-2xl font-semibold text-white">{stat.value}</p></div>)}</div><div className="mt-5 rounded-2xl border border-blue-500/30 bg-blue-500/10 p-4 text-sm text-blue-100">{metrics?.scale_note || 'Relative monocular scale only unless an external scale source is provided.'}</div><div className="mt-5 flex flex-wrap gap-3"><a className="inline-flex rounded-xl bg-blue-500 px-4 py-2 font-medium text-white transition hover:bg-blue-400" href={`${apiBase}/api/jobs/${jobId}/pointcloud`}>Open sparse PLY</a><a className="inline-flex rounded-xl border border-slate-600 px-4 py-2 font-medium text-slate-200 transition hover:border-blue-300 hover:bg-slate-800" href={`${apiBase}/api/jobs/${jobId}/pointcloud?dense=true`}>Open dense PLY</a></div></div>;
}
