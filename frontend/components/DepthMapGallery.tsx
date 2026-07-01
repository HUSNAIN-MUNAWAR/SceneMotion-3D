export default function DepthMapGallery({ maps }: { maps: string[] }) {
  return <div className="card p-6"><h2 className="font-semibold text-white">Depth maps</h2><div className="mt-4 grid gap-4 md:grid-cols-2">{maps.map(src => <img key={src} src={src} alt="Depth map" className="rounded-2xl border border-slate-700 bg-slate-950" />)}</div></div>;
}
