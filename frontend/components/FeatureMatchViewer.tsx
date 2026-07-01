export default function FeatureMatchViewer({ images }: { images: string[] }) {
  return <div className="card p-6"><h2 className="font-semibold text-white">Feature matches</h2><div className="mt-4 grid gap-4 lg:grid-cols-2">{images.map(src => <img key={src} src={src} alt="Feature match visualization" className="rounded-2xl border border-slate-700 bg-slate-950" />)}</div></div>;
}
