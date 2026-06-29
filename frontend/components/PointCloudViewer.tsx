'use client';
export default function PointCloudViewer({ jobId, apiBase }: { jobId: string; apiBase: string }) {
  return <div className="card p-6"><h2 className="font-semibold text-white">3D point cloud viewer</h2><div className="mt-4 h-72 rounded-xl border border-slate-700 bg-slate-950 p-4"><p className="text-sm text-slate-400">The viewer loads exported PLY artifacts from the backend. A production deployment can attach Three.js PLYLoader here; this fallback keeps the UI usable without WebGL-specific dependencies during static validation.</p><a className="mt-4 inline-block rounded-lg bg-blue-500 px-4 py-2 text-white" href={`${apiBase}/api/jobs/${jobId}/pointcloud`}>Open sparse PLY</a></div></div>;
}
