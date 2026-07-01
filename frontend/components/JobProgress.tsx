export default function JobProgress({ job }: { job: any }) {
  const progress = job?.progress ?? 0;
  return <div className="card p-6"><div className="flex justify-between"><h2 className="font-semibold text-white">Progress</h2><span>{progress}%</span></div><div className="mt-4 h-3 rounded-full bg-slate-800"><div className="h-3 rounded-full bg-blue-500" style={{width: `${progress}%`}} /></div><p className="mt-3 text-sm text-slate-400">{job?.stage || 'Waiting'} - {job?.message || ''}</p>{job?.error && <p className="mt-3 text-red-300">{job.error}</p>}</div>;
}
