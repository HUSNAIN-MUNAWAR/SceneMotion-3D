'use client';

import Link from 'next/link';
import { useEffect, useState } from 'react';

import SampleVideoSelector from '@/components/SampleVideoSelector';
import VideoUpload from '@/components/VideoUpload';
import { DEMO_JOB_ID, getSamples, startSampleJob } from '@/lib/api';

export default function UploadPage() {
  const [samples, setSamples] = useState<any[]>([]);
  const [error, setError] = useState<string>('');

  useEffect(() => {
    getSamples().then(setSamples).catch(e => setError(e.message));
  }, []);

  async function start(name: string) {
    const job = await startSampleJob(name);
    window.location.href = `/jobs/${job.job_id}`;
  }

  return <main className="min-h-screen p-8"><div className="mx-auto max-w-6xl"><div className="grid gap-6 lg:grid-cols-[1.1fr_0.9fr]"><section className="card overflow-hidden p-8"><p className="text-sm uppercase tracking-[0.28em] text-blue-300">Run Pipeline</p><h1 className="mt-4 text-4xl font-semibold text-white">Upload footage or launch the bundled synthetic scene.</h1><p className="mt-4 max-w-3xl text-base leading-7 text-slate-300">This workspace includes a completed demo run for instant review plus a sample video for launching a fresh reconstruction job through the real backend.</p><div className="mt-6 flex flex-wrap gap-3"><Link href={`/jobs/${DEMO_JOB_ID}`} className="rounded-xl bg-blue-500 px-5 py-3 font-semibold text-white transition hover:bg-blue-400">Open completed demo run</Link><Link href="/docs" className="rounded-xl border border-slate-600 px-5 py-3 font-semibold text-slate-200 transition hover:border-blue-300 hover:bg-slate-900">Read limitations</Link></div>{error && <p className="mt-5 rounded-xl border border-red-500/30 bg-red-950/70 p-4 text-sm text-red-200">{error}</p>}<div className="mt-8 grid gap-6 md:grid-cols-2"><VideoUpload /><SampleVideoSelector samples={samples} onStart={start} /></div></section><aside className="space-y-6"><div className="card p-6"><h2 className="text-xl font-semibold text-white">What this flow produces</h2><div className="mt-4 grid gap-3">{['Trajectory JSON with per-pose transforms', 'Sparse and dense point cloud exports', 'Feature-match visualizations and quality warnings', 'HTML/PDF reports plus downloadable run bundle'].map(item => <div key={item} className="rounded-2xl border border-slate-800 bg-slate-950/50 p-4 text-sm text-slate-200">{item}</div>)}</div></div><div className="card p-6"><h2 className="text-xl font-semibold text-white">Recommended reviewer path</h2><ol className="mt-4 space-y-3 text-sm text-slate-300"><li>1. Open the bundled demo run to inspect the completed reconstruction.</li><li>2. Visit feature matches, depth, point cloud, and reports pages to verify the artifacts.</li><li>3. Start a new sample run from this page if you want to see the job lifecycle.</li></ol></div></aside></div></div></main>;
}
