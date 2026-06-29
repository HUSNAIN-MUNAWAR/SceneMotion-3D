export default function StageTimingChart({ timings = {} as Record<string, number> }) {
  const entries = Object.entries(timings)
  const max = Math.max(0.001, ...entries.map(([,v]) => Number(v)))
  return <div className="rounded-2xl border border-slate-700 bg-slate-900 p-4"><h3 className="text-lg font-semibold">Stage timing</h3>{entries.map(([k,v]) => <div key={k} className="my-2"><div className="flex justify-between text-xs text-slate-400"><span>{k}</span><span>{Number(v).toFixed(3)}s</span></div><div className="h-2 rounded bg-slate-800"><div className="h-2 rounded bg-sky-500" style={{width: `${Math.max(4, Number(v)/max*100)}%`}} /></div></div>)}</div>
}
