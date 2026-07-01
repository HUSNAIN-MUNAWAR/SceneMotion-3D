import Link from 'next/link';

const stats = [
  { label: 'Selected keyframes', value: '8' },
  { label: 'Sparse 3D points', value: '3,371' },
  { label: 'Dense cloud points', value: '4,240' },
];

const highlights = [
  'Real ORB / SIFT / AKAZE feature pipelines, matching, and RANSAC filtering',
  'Monocular pose chaining, triangulation, sparse reconstruction, and dense cloud export',
  'Benchmark-style metrics, artifact bundles, warnings, and report generation',
];

const routes = [
  { href: '/jobs/demo_job_synthetic', label: 'Live demo run' },
  { href: '/matches', label: 'Feature matches' },
  { href: '/depth', label: 'Depth explorer' },
  { href: '/reports', label: 'Reports' },
];

export default function LandingPage() {
  return <main className="min-h-screen px-6 py-8 md:px-10"><section className="mx-auto max-w-6xl"><div className="flex flex-wrap items-center justify-between gap-4 rounded-full border border-slate-800/80 bg-slate-950/60 px-5 py-3 backdrop-blur"><div><p className="text-xs uppercase tracking-[0.32em] text-blue-300">SceneMotion-3D</p><p className="mt-1 text-sm text-slate-400">Production-style monocular reconstruction demo</p></div><nav className="flex flex-wrap gap-2 text-sm">{routes.map(route => <Link key={route.href} href={route.href} className="rounded-full border border-slate-700 px-4 py-2 text-slate-200 transition hover:border-blue-400 hover:text-white">{route.label}</Link>)}</nav></div><div className="mt-8 overflow-hidden rounded-[2rem] border border-slate-800/80 bg-[linear-gradient(135deg,rgba(15,23,42,0.96),rgba(15,23,42,0.76)),radial-gradient(circle_at_top_left,rgba(37,99,235,0.28),transparent_32%),radial-gradient(circle_at_bottom_right,rgba(14,116,144,0.22),transparent_24%)] p-8 shadow-[0_30px_80px_rgba(15,23,42,0.45)] md:p-12"><div className="grid gap-10 lg:grid-cols-[1.15fr_0.85fr]"><div><p className="text-sm uppercase tracking-[0.35em] text-blue-300">Core Computer Vision Portfolio</p><h1 className="mt-5 max-w-3xl text-4xl font-semibold leading-tight text-white md:text-6xl">SceneMotion-3D turns a monocular video into trajectories, reconstructions, depth-assisted clouds, and evidence-rich reports.</h1><p className="mt-6 max-w-3xl text-lg leading-8 text-slate-300">This project is built around real geometry-heavy CV work: feature extraction, correspondence filtering, essential matrix estimation, pose recovery, triangulation, local refinement, and honest scale reporting.</p><div className="mt-8 flex flex-wrap gap-4"><Link href="/jobs/demo_job_synthetic" className="inline-flex items-center rounded-2xl bg-blue-500 px-6 py-3 text-base font-semibold text-white transition hover:bg-blue-400">Open live demo run</Link><Link href="/upload" className="inline-flex items-center rounded-2xl border border-slate-600 px-6 py-3 text-base font-semibold text-slate-100 transition hover:border-blue-300 hover:bg-slate-900/70">Upload or test a video</Link></div><div className="mt-10 grid gap-4 md:grid-cols-3">{stats.map(stat => <div key={stat.label} className="rounded-2xl border border-slate-800 bg-slate-950/45 p-4"><p className="text-xs uppercase tracking-[0.24em] text-slate-500">{stat.label}</p><p className="mt-3 text-3xl font-semibold text-white">{stat.value}</p></div>)}</div></div><div className="space-y-4 rounded-[1.75rem] border border-slate-800 bg-slate-950/45 p-6"><p className="text-sm uppercase tracking-[0.28em] text-cyan-300">About This Build</p><h2 className="text-2xl font-semibold text-white">A reviewer can inspect the pipeline, the artifacts, and the limitations instead of trusting a black box.</h2><p className="text-sm leading-7 text-slate-300">The bundled demo run ships with metrics, trajectory poses, match visualizations, depth maps, point clouds, loop-closure metadata, and PDF/HTML reports. That makes the About section practical: the blue button above opens a real completed run, not a mock page.</p><div className="space-y-3 pt-2">{highlights.map(item => <div key={item} className="rounded-2xl border border-slate-800 bg-slate-900/70 px-4 py-3 text-sm text-slate-200">{item}</div>)}</div><Link href="/reports" className="mt-2 inline-flex items-center rounded-2xl bg-blue-600 px-5 py-3 text-sm font-semibold text-white transition hover:bg-blue-500">Review metrics, warnings, and reports</Link></div></div></div></section></main>;
}
