'use client';
import { useState } from 'react';
import { API_BASE } from '@/lib/api';
export default function VideoUpload() {
  const [status, setStatus] = useState('Choose an MP4/MOV/AVI/MKV file under the configured upload limit.');
  async function onChange(e: React.ChangeEvent<HTMLInputElement>) {
    const file = e.target.files?.[0];
    if (!file) return;
    const form = new FormData(); form.append('file', file);
    setStatus('Uploading...');
    const res = await fetch(`${API_BASE}/api/videos/upload`, { method: 'POST', body: form });
    if (!res.ok) { setStatus('Upload failed. Check file type and size.'); return; }
    const data = await res.json();
    const start = await fetch(`${API_BASE}/api/jobs/start`, { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({ source: 'uploaded', upload_id: data.upload_id }) });
    const job = await start.json();
    window.location.href = `/jobs/${job.job_id}`;
  }
  return <div className="card p-6"><h2 className="text-xl font-semibold text-white">Upload local video</h2><input className="mt-4 block w-full rounded-lg border border-slate-700 p-3" type="file" accept="video/*" onChange={onChange}/><p className="mt-3 text-sm text-slate-400">{status}</p></div>;
}
