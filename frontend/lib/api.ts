export const API_BASE = process.env.NEXT_PUBLIC_API_BASE || 'http://localhost:8000';

export async function getSamples() {
  const res = await fetch(`${API_BASE}/api/videos/samples`, { cache: 'no-store' });
  if (!res.ok) throw new Error('Failed to load samples');
  return res.json();
}

export async function startSampleJob(sampleName: string) {
  const res = await fetch(`${API_BASE}/api/jobs/start`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ source: 'sample', sample_name: sampleName })
  });
  if (!res.ok) throw new Error('Failed to start job');
  return res.json();
}

export async function getJob(jobId: string) {
  const res = await fetch(`${API_BASE}/api/jobs/${jobId}`, { cache: 'no-store' });
  if (!res.ok) throw new Error('Failed to load job');
  return res.json();
}

export async function getMetrics(jobId: string) {
  const res = await fetch(`${API_BASE}/api/jobs/${jobId}/metrics`, { cache: 'no-store' });
  if (!res.ok) throw new Error('Metrics are not ready');
  return res.json();
}
