'use client';

import { useEffect, useState } from 'react';

import PointCloudViewer from '@/components/PointCloudViewer';
import TrajectoryViewer from '@/components/TrajectoryViewer';
import { API_BASE, DEMO_JOB_ID, getMetrics, getTrajectory, type JobMetrics, type TrajectoryPayload } from '@/lib/api';

export default function PointCloudPage() {
  const [metrics, setMetrics] = useState<JobMetrics | null>(null);
  const [trajectory, setTrajectory] = useState<TrajectoryPayload | null>(null);
  const [error, setError] = useState('');

  useEffect(() => {
    Promise.all([getMetrics(DEMO_JOB_ID), getTrajectory(DEMO_JOB_ID)])
      .then(([metricData, trajectoryData]) => {
        setMetrics(metricData);
        setTrajectory(trajectoryData);
      })
      .catch(e => setError(e.message));
  }, []);

  return <main className="min-h-screen p-8"><div className="mx-auto max-w-6xl"><p className="text-sm uppercase tracking-[0.28em] text-blue-300">Trajectory And Point Cloud</p><h1 className="mt-3 text-4xl font-semibold text-white">Sparse and dense geometry from the completed demo job</h1><p className="mt-3 max-w-4xl text-base leading-7 text-slate-300">The viewer below points to the real exported PLY files, while the trajectory panel shows the recovered camera path coordinates from `trajectory.json`.</p>{error && <p className="mt-5 rounded-xl border border-red-500/30 bg-red-950/70 p-4 text-sm text-red-200">{error}</p>}<div className="mt-8 space-y-6"><PointCloudViewer jobId={DEMO_JOB_ID} apiBase={API_BASE} metrics={metrics || undefined} /><TrajectoryViewer positions={trajectory?.positions || []} /><div className="card p-6"><h2 className="text-lg font-semibold text-white">Reconstruction notes</h2><div className="mt-4 grid gap-4 md:grid-cols-3">{[{ label: 'Trajectory length', value: trajectory?.trajectory_length_relative ?? 0 }, { label: 'Scale mode', value: metrics?.scale_mode ?? 'relative' }, { label: 'Loop candidates', value: metrics?.loop_candidates ?? 0 }].map(card => <div key={card.label} className="rounded-2xl border border-slate-800 bg-slate-950/50 p-4"><p className="text-xs uppercase tracking-[0.24em] text-slate-500">{card.label}</p><p className="mt-2 text-2xl font-semibold text-white">{card.value}</p></div>)}</div><p className="mt-5 text-sm leading-7 text-slate-300">{trajectory?.scale_note || metrics?.scale_note || 'Relative monocular units only.'}</p></div></div></div></main>;
}
