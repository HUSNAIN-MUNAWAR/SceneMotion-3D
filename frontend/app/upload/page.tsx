'use client';
import { useEffect, useState } from 'react';
import { getSamples, startSampleJob } from '@/lib/api';
import VideoUpload from '@/components/VideoUpload';
import SampleVideoSelector from '@/components/SampleVideoSelector';

export default function UploadPage() {
  const [samples, setSamples] = useState<any[]>([]);
  const [error, setError] = useState<string>('');
  useEffect(() => { getSamples().then(setSamples).catch(e => setError(e.message)); }, []);
  async function start(name: string) {
    const job = await startSampleJob(name);
    window.location.href = `/jobs/${job.job_id}`;
  }
  return <main className="min-h-screen p-8"><div className="mx-auto max-w-5xl">
    <h1 className="text-3xl font-bold text-white">Upload or select video</h1>
    {error && <p className="mt-4 rounded-lg bg-red-950 p-4 text-red-200">{error}</p>}
    <div className="mt-6 grid gap-6 md:grid-cols-2">
      <VideoUpload />
      <SampleVideoSelector samples={samples} onStart={start} />
    </div>
  </div></main>;
}
