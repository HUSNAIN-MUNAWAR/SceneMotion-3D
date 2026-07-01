'use client';

import { useEffect, useState } from 'react';

import DepthMapGallery from '@/components/DepthMapGallery';
import { DEMO_JOB_ID, getArtifacts, getMetrics, jobArtifactUrl, type ArtifactIndex, type JobMetrics } from '@/lib/api';

export default function DepthPage() {
  const [artifacts, setArtifacts] = useState<ArtifactIndex | null>(null);
  const [metrics, setMetrics] = useState<JobMetrics | null>(null);
  const [error, setError] = useState('');

  useEffect(() => {
    Promise.all([getArtifacts(DEMO_JOB_ID), getMetrics(DEMO_JOB_ID)])
      .then(([artifactData, metricData]) => {
        setArtifacts(artifactData);
        setMetrics(metricData);
      })
      .catch(e => setError(e.message));
  }, []);

  const maps = (artifacts?.depth_maps || []).map(path => jobArtifactUrl(DEMO_JOB_ID, path));

  return <main className="min-h-screen p-8"><div className="mx-auto max-w-6xl"><p className="text-sm uppercase tracking-[0.28em] text-blue-300">Depth Explorer</p><h1 className="mt-3 text-4xl font-semibold text-white">Real depth maps from the bundled demo run</h1><p className="mt-3 max-w-3xl text-base leading-7 text-slate-300">The default provider is the offline-safe pseudo-depth fallback included with this repo. The screen below shows the actual generated PNG depth outputs and the dense cloud totals that came from them.</p>{error && <p className="mt-5 rounded-xl border border-red-500/30 bg-red-950/70 p-4 text-sm text-red-200">{error}</p>}<div className="mt-8 grid gap-4 md:grid-cols-3">{[{ label: 'Depth maps generated', value: metrics?.depth_maps_generated ?? 0 }, { label: 'Dense cloud points', value: metrics?.dense_cloud_point_count ?? 0 }, { label: 'Depth provider', value: metrics?.depth_provider ?? 'fallback_pseudo_depth' }].map(card => <div key={card.label} className="card p-5"><p className="text-xs uppercase tracking-[0.24em] text-slate-500">{card.label}</p><p className="mt-3 text-2xl font-semibold text-white">{card.value}</p></div>)}</div><div className="mt-8">{maps.length > 0 ? <DepthMapGallery maps={maps} /> : <div className="card p-6 text-sm text-slate-400">Loading depth maps...</div>}</div></div></main>;
}
