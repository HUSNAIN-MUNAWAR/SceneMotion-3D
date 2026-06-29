'use client';
import { useEffect, useState } from 'react';
import { getJob, getMetrics, API_BASE } from '@/lib/api';
import JobProgress from '@/components/JobProgress';
import PipelineStageStepper from '@/components/PipelineStageStepper';
import MetricsCards from '@/components/MetricsCards';
import WarningPanel from '@/components/WarningPanel';
import ArtifactDownloads from '@/components/ArtifactDownloads';
import PointCloudViewer from '@/components/PointCloudViewer';

export default function JobPage({ params }: { params: { jobId: string } }) {
  const [job, setJob] = useState<any>(null);
  const [metrics, setMetrics] = useState<any>(null);
  useEffect(() => {
    const id = setInterval(async () => {
      const j = await getJob(params.jobId); setJob(j);
      if (j.status === 'completed') { try { setMetrics(await getMetrics(params.jobId)); } catch {} }
    }, 1200);
    return () => clearInterval(id);
  }, [params.jobId]);
  return <main className="min-h-screen p-8"><div className="mx-auto max-w-7xl">
    <h1 className="text-3xl font-bold text-white">Reconstruction Job</h1>
    <p className="mt-2 text-slate-400">{params.jobId}</p>
    <div className="mt-6 grid gap-6 lg:grid-cols-[1fr_360px]">
      <section className="space-y-6">
        <JobProgress job={job} />
        <PipelineStageStepper stage={job?.stage} />
        {metrics && <MetricsCards metrics={metrics} />}
        {metrics && <PointCloudViewer jobId={params.jobId} apiBase={API_BASE} />}
      </section>
      <aside className="space-y-6">
        <WarningPanel warnings={metrics?.warnings || job?.warnings || []} />
        <ArtifactDownloads jobId={params.jobId} />
      </aside>
    </div>
  </div></main>;
}
