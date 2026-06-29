const stages = ['frame_extraction','keyframes','features','matching','visual_odometry','sparse_reconstruction','depth','dense_cloud','reports','completed'];
export default function PipelineStageStepper({ stage }: { stage?: string }) {
  const idx = stages.indexOf(stage || '');
  return <div className="card p-6"><h2 className="font-semibold text-white">Pipeline stages</h2><div className="mt-4 grid gap-2 md:grid-cols-2">{stages.map((s, i) => <div key={s} className={`rounded-lg border p-3 text-sm ${i <= idx ? 'border-blue-500 bg-blue-950/40' : 'border-slate-700'}`}>{s.replaceAll('_',' ')}</div>)}</div></div>;
}
