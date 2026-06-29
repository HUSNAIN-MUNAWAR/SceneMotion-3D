import Link from 'next/link';
export default function LandingPage() {
  return <main className="min-h-screen px-8 py-10 bg-[radial-gradient(circle_at_top,#1e3a8a33,transparent_40%)]">
    <section className="mx-auto max-w-6xl">
      <div className="card p-10 shadow-glow">
        <p className="text-sm uppercase tracking-[0.3em] text-blue-300">Core Computer Vision Portfolio</p>
        <h1 className="mt-6 text-5xl font-bold text-white">SceneMotion 3D</h1>
        <p className="mt-4 max-w-3xl text-lg text-slate-300">Monocular visual odometry, depth estimation, Structure-from-Motion concepts, point clouds, trajectory estimation, metrics, reports, and honest limitations.</p>
        <div className="mt-8 flex gap-4">
          <Link href="/upload" className="rounded-xl bg-blue-500 px-5 py-3 font-semibold text-white hover:bg-blue-400">Start reconstruction</Link>
          <Link href="/docs" className="rounded-xl border border-slate-600 px-5 py-3 text-slate-200 hover:bg-slate-800">Read limitations</Link>
        </div>
      </div>
      <div className="mt-8 grid gap-4 md:grid-cols-3">
        {['Feature matching + RANSAC', 'Essential matrix + pose', 'Sparse/dense point clouds'].map(x => <div key={x} className="card p-6"><h3 className="font-semibold text-white">{x}</h3><p className="mt-2 text-sm text-slate-400">Implemented with real APIs and offline-safe demo behavior.</p></div>)}
      </div>
    </section>
  </main>;
}
