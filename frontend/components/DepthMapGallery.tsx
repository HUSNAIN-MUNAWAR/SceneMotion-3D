export default function DepthMapGallery({ maps }: { maps: string[] }) {
  return <div className="card p-6"><h2 className="font-semibold text-white">Depth maps</h2><div className="mt-3 grid gap-3 md:grid-cols-2">{maps.map(src => <img key={src} src={src} alt="Depth map" className="rounded-lg border border-slate-700" />)}</div></div>;
}
