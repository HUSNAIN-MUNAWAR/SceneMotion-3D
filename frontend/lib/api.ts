export const API_BASE = process.env.NEXT_PUBLIC_API_BASE || 'http://localhost:8000';
export const DEMO_JOB_ID = process.env.NEXT_PUBLIC_DEMO_JOB_ID || 'demo_job_synthetic';

export type ArtifactIndex = {
  job_output_dir?: string;
  metrics?: string;
  trajectory?: string;
  reports?: string[];
  pointclouds?: string[];
  depth_maps?: string[];
  match_visualizations?: string[];
  quality_report?: string;
  loop_candidates?: string;
  bundle?: string;
};

export type QualityNarrative = {
  reconstruction_quality_grade?: string;
  tracking_stability?: number;
  scale_mode?: string;
  likely_failure_reasons?: string[];
  recommended_fixes?: string[];
};

export type JobMetrics = Record<string, any> & {
  timing_profile?: Record<string, number>;
  warnings?: string[];
  quality_narrative?: QualityNarrative;
};

export type JobState = {
  job_id: string;
  status: 'queued' | 'running' | 'completed' | 'failed';
  progress: number;
  stage: string;
  message?: string;
  warnings?: string[];
  error?: string | null;
};

export type TrajectoryPayload = {
  positions: number[][];
  poses?: Array<Record<string, any>>;
  trajectory_length_relative?: number;
  scale_note?: string;
};

async function readJson<T>(url: string, errorMessage: string): Promise<T> {
  const res = await fetch(url, { cache: 'no-store' });
  if (!res.ok) {
    throw new Error(errorMessage);
  }
  return res.json();
}

function encodeArtifactPath(path: string) {
  return path.split('/').map(part => encodeURIComponent(part)).join('/');
}

export function jobArtifactUrl(jobId: string, path: string) {
  return `${API_BASE}/api/jobs/${jobId}/artifact/${encodeArtifactPath(path)}`;
}

export function jobReportUrl(jobId: string, fmt: 'html' | 'pdf' = 'html') {
  return `${API_BASE}/api/jobs/${jobId}/report?fmt=${fmt}`;
}

export function jobPointCloudUrl(jobId: string, dense = false) {
  return `${API_BASE}/api/jobs/${jobId}/pointcloud${dense ? '?dense=true' : ''}`;
}

export function jobBundleUrl(jobId: string) {
  return `${API_BASE}/api/jobs/${jobId}/bundle`;
}

export async function getSamples() {
  return readJson<any[]>(`${API_BASE}/api/videos/samples`, 'Failed to load samples');
}

export async function startSampleJob(sampleName: string) {
  const res = await fetch(`${API_BASE}/api/jobs/start`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ source: 'sample', sample_name: sampleName }),
  });
  if (!res.ok) {
    throw new Error('Failed to start job');
  }
  return res.json();
}

export async function getJob(jobId: string) {
  return readJson<JobState>(`${API_BASE}/api/jobs/${jobId}`, 'Failed to load job');
}

export async function getMetrics(jobId: string) {
  return readJson<JobMetrics>(`${API_BASE}/api/jobs/${jobId}/metrics`, 'Metrics are not ready');
}

export async function getArtifacts(jobId: string) {
  return readJson<ArtifactIndex>(`${API_BASE}/api/jobs/${jobId}/artifacts`, 'Artifacts are not ready');
}

export async function getTrajectory(jobId: string) {
  return readJson<TrajectoryPayload>(`${API_BASE}/api/jobs/${jobId}/trajectory`, 'Trajectory is not ready');
}
