export default function WarningPanel({ warnings }: { warnings: string[] }) {
  return <div className="card p-6"><h2 className="font-semibold text-white">Warnings</h2>{warnings.length === 0 ? <p className="mt-3 text-sm text-slate-400">Warnings appear after metrics are generated.</p> : <ul className="mt-3 list-disc space-y-2 pl-5 text-sm text-amber-200">{warnings.map(w => <li key={w}>{w}</li>)}</ul>}</div>;
}
