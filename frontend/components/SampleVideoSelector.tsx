'use client';
export default function SampleVideoSelector({ samples, onStart }: { samples: any[]; onStart: (name: string) => void }) {
  return <div className="card p-6"><h2 className="text-xl font-semibold text-white">Sample videos</h2><div className="mt-4 space-y-3">{samples.length === 0 && <p className="text-sm text-slate-400">No sample videos found. Run make generate-sample.</p>}{samples.map(s => <button key={s.name} onClick={() => onStart(s.name)} className="flex w-full items-center justify-between rounded-xl border border-slate-700 p-4 text-left hover:bg-slate-800"><span>{s.name}</span><span className="text-sm text-blue-300">Run</span></button>)}</div></div>;
}
