'use client';

import Link from 'next/link';
import { useEffect, useState } from 'react';

import ArtifactDownloads from '@/components/ArtifactDownloads';
import JobProgress from '@/components/JobProgress';
import MetricsCards from '@/components/MetricsCards';
import PipelineStageStepper from '@/components/PipelineStageStepper';
import PointCloudViewer from '@/components/PointCloudViewer';
import WarningPanel from '@/components/WarningPanel';
import { API_BASE, getJob, getMetrics } from '@/lib/api';

const demoLinks = [
  { href: '/matches', label: 'Feature matches' },
  { href: '/depth', label: 'Depth explorer' },
  { href: '/pointcloud', label: 'Point clouds' },
  { href: '/reports', label: 'Reports' },
];

export default function JobPage({ params }: { params: { jobId: string } }) {
  const [job, setJob] = useState<any>(null);
  const [metrics, setMetrics] = useState<any>(null);

  useEffect(() => {
    const id = setInterval(async () => {
      const currentJob = await getJob(params.jobId);
      setJob(currentJob);
      if (currentJob.status === 'completed') {
        try {
          setMetrics(await getMetrics(params.jobId));
        } catch {}
      }
    }, 1200);

    return () => clearInterval(id);
  }, [params.jobId]);

  return <main className="min-h-screen p-8"><div className="mx-auto max-w-7xl"><div className="flex flex-wrap items-end justify-between gap-4"><div><p className="text-sm uppercase tracking-[0.28em] text-blue-300">Reconstruction Job</p><h1 className="mt-3 text-4xl font-semibold text-white">{params.jobId}</h1><p className="mt-3 max-w-4xl text-base leading-7 text-slate-300">Live job status, pipeline progress, metrics, warnings, and artifact downloads for this reconstruction run.</p></div><div className="flex flex-wrap gap-2">{demoLinks.map(link => <Link key={link.href} href={link.href} className="rounded-full border border-slate-700 px-4 py-2 text-sm text-slate-200 transition hover:border-blue-400 hover:text-white">{link.label}</Link>)}</div></div><div className="mt-6 grid gap-6 lg:grid-cols-[1fr_360px]"><section className="space-y-6"><JobProgress job={job} /><PipelineStageStepper stage={job?.stage} />{metrics && <MetricsCards metrics={metrics} />}{metrics && <PointCloudViewer jobId={params.jobId} apiBase={API_BASE} metrics={metrics} />}</section><aside className="space-y-6"><WarningPanel warnings={metrics?.warnings || job?.warnings || []} /><ArtifactDownloads jobId={params.jobId} /></aside></div></div></main>;
}
