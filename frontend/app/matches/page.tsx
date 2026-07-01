'use client';

import { useEffect, useState } from 'react';

import FeatureMatchViewer from '@/components/FeatureMatchViewer';
import { DEMO_JOB_ID, getArtifacts, getMetrics, jobArtifactUrl, type ArtifactIndex, type JobMetrics } from '@/lib/api';

export default function MatchViewerPage() {
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

  const images = (artifacts?.match_visualizations || []).map(path => jobArtifactUrl(DEMO_JOB_ID, path));

  return <main className="min-h-screen p-8"><div className="mx-auto max-w-6xl"><div className="flex flex-wrap items-end justify-between gap-4"><div><p className="text-sm uppercase tracking-[0.28em] text-blue-300">Demo Artifacts</p><h1 className="mt-3 text-4xl font-semibold text-white">Feature match viewer</h1><p className="mt-3 max-w-3xl text-base leading-7 text-slate-300">These images come from the completed synthetic run and show the actual correspondences used before pose estimation and triangulation.</p></div></div>{error && <p className="mt-5 rounded-xl border border-red-500/30 bg-red-950/70 p-4 text-sm text-red-200">{error}</p>}<div className="mt-8 grid gap-4 md:grid-cols-3">{[{ label: 'Pose pairs', value: metrics?.valid_pose_pairs ?? 0 }, { label: 'Avg matches / pair', value: metrics?.average_matches_per_pair ? Number(metrics.average_matches_per_pair).toFixed(0) : '0' }, { label: 'Avg inlier ratio', value: metrics?.average_inlier_ratio ? Number(metrics.average_inlier_ratio).toFixed(3) : '0.000' }].map(card => <div key={card.label} className="card p-5"><p className="text-xs uppercase tracking-[0.24em] text-slate-500">{card.label}</p><p className="mt-3 text-3xl font-semibold text-white">{card.value}</p></div>)}</div><div className="mt-8">{images.length > 0 ? <FeatureMatchViewer images={images} /> : <div className="card p-6 text-sm text-slate-400">Loading match visualizations...</div>}</div></div></main>;
}
