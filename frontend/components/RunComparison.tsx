type Row = { metric: string; runA: string | number; runB: string | number; delta?: string | number }

export default function RunComparison({ rows = [] as Row[] }) {
  return <div className="rounded-2xl border border-slate-700 bg-slate-900 p-4"><h3 className="text-lg font-semibold">Run comparison</h3><table className="mt-3 w-full text-sm"><tbody>{rows.map(row => <tr key={row.metric} className="border-t border-slate-800"><td className="py-2 text-slate-300">{row.metric}</td><td>{row.runA}</td><td>{row.runB}</td><td>{row.delta ?? '-'}</td></tr>)}</tbody></table></div>;
}
