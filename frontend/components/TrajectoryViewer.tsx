export default function TrajectoryViewer({ positions }: { positions: number[][] }) {
  return <div className="card p-6"><h2 className="font-semibold text-white">Trajectory</h2><pre className="mt-3 max-h-64 overflow-auto rounded bg-slate-950 p-3 text-xs">{JSON.stringify(positions?.slice(0, 20) || [], null, 2)}</pre></div>;
}
