export default function FeatureMatchViewer({ images }: { images: string[] }) {
  return <div className="card p-6"><h2 className="font-semibold text-white">Feature matches</h2><div className="mt-3 grid gap-3">{images.map(src => <img key={src} src={src} alt="Feature match visualization" className="rounded-lg border border-slate-700" />)}</div></div>;
}
