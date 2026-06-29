import PointCloudViewer from '@/components/PointCloudViewer';
export default function PointCloudPage() {
  return <main className="min-h-screen p-8"><div className="mx-auto max-w-5xl"><h1 className="text-3xl font-bold text-white">3D Point Cloud Viewer</h1><p className="mt-3 text-slate-400">Use a completed job ID to download sparse or dense PLY artifacts.</p><PointCloudViewer jobId="demo_job_synthetic" apiBase="http://localhost:8000" /></div></main>;
}
