'use client';

import { useEffect, useState } from 'react';

import ArtifactDownloads from '@/components/ArtifactDownloads';
import MetricsCards from '@/components/MetricsCards';
import ScaleModeCard from '@/components/ScaleModeCard';
import StageTimingChart from '@/components/StageTimingChart';
import WarningPanel from '@/components/WarningPanel';
import { DEMO_JOB_ID, getMetrics, jobReportUrl, type JobMetrics } from '@/lib/api';

export default function ReportsPage() {
  const [metrics, setMetrics] = useState<JobMetrics | null>(null);
  const [error, setError] = useState('');

  useEffect(() => {
    getMetrics(DEMO_JOB_ID).then(setMetrics).catch(e => setError(e.message));
  }, []);

  const recommendedFixes = metrics?.quality_narrative?.recommended_fixes || [];
  const failureReasons = metrics?.quality_narrative?.likely_failure_reasons || [];

  return <main className="min-h-screen p-8"><div className="mx-auto max-w-7xl"><div><p className="text-sm uppercase tracking-[0.28em] text-blue-300">Reports And Metrics</p><h1 className="mt-3 text-4xl font-semibold text-white">Evaluation dashboard for the shipped demo reconstruction</h1><p className="mt-3 max-w-4xl text-base leading-7 text-slate-300">This page is wired to the real `demo_job_synthetic` metrics and report artifacts stored in the repo. The preview below loads the actual generated HTML report from the backend.</p></div>{error && <p className="mt-5 rounded-xl border border-red-500/30 bg-red-950/70 p-4 text-sm text-red-200">{error}</p>}<div className="mt-8 grid gap-6 xl:grid-cols-[1.25fr_0.75fr]"><section className="space-y-6"><div className="card p-6">{metrics ? <MetricsCards metrics={metrics} /> : <p className="text-sm text-slate-400">Loading metrics...</p>}</div>{metrics?.timing_profile && <StageTimingChart timings={metrics.timing_profile} />}<div className="card overflow-hidden p-4"><div className="flex items-center justify-between gap-4 border-b border-slate-800 px-2 pb-4"><div><h2 className="text-lg font-semibold text-white">HTML report preview</h2><p className="mt-1 text-sm text-slate-400">Live preview of the generated benchmark-style report.</p></div><a href={jobReportUrl(DEMO_JOB_ID)} className="rounded-xl bg-blue-500 px-4 py-2 text-sm font-semibold text-white transition hover:bg-blue-400">Open report tab</a></div><iframe title="SceneMotion 3D HTML report preview" src={jobReportUrl(DEMO_JOB_ID)} className="mt-4 h-[720px] w-full rounded-2xl border border-slate-800 bg-white" /></div></section><aside className="space-y-6"><ScaleModeCard /><div className="card p-6"><h2 className="text-lg font-semibold text-white">Quality narrative</h2><div className="mt-4 space-y-4 text-sm text-slate-300"><p><span className="text-slate-500">Grade:</span> {metrics?.quality_narrative?.reconstruction_quality_grade || 'loading'}</p><p><span className="text-slate-500">Tracking stability:</span> {metrics?.quality_narrative?.tracking_stability ? Number(metrics.quality_narrative.tracking_stability).toFixed(3) : '0.000'}</p><p><span className="text-slate-500">Scale mode:</span> {metrics?.quality_narrative?.scale_mode || 'relative'}</p></div><div className="mt-5"><h3 className="text-sm font-semibold uppercase tracking-[0.24em] text-slate-500">Recommended fixes</h3><ul className="mt-3 space-y-2 text-sm text-slate-300">{recommendedFixes.map(item => <li key={item} className="rounded-xl border border-slate-800 bg-slate-950/40 px-3 py-2">{item}</li>)}{recommendedFixes.length === 0 && <li className="text-slate-500">No recommendations recorded.</li>}</ul></div><div className="mt-5"><h3 className="text-sm font-semibold uppercase tracking-[0.24em] text-slate-500">Likely failure reasons</h3><ul className="mt-3 space-y-2 text-sm text-slate-300">{failureReasons.map(item => <li key={item} className="rounded-xl border border-slate-800 bg-slate-950/40 px-3 py-2">{item}</li>)}{failureReasons.length === 0 && <li className="text-slate-500">No failure reasons were triggered for this run.</li>}</ul></div></div><WarningPanel warnings={metrics?.warnings || []} /><ArtifactDownloads jobId={DEMO_JOB_ID} /></aside></div></div></main>;
}
