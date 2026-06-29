import TrajectoryViewer from '@/components/TrajectoryViewer';
export default function VODashboardPage() {
  return <main className="min-h-screen p-8"><div className="mx-auto max-w-5xl"><h1 className="text-3xl font-bold text-white">Visual Odometry Dashboard</h1><p className="mt-3 text-slate-400">Open a completed job page to load live trajectory JSON from the backend. This page documents the VO view structure.</p><TrajectoryViewer positions={[]} /></div></main>;
}
