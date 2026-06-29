import DepthMapGallery from '@/components/DepthMapGallery';
export default function DepthPage() {
  return <main className="min-h-screen p-8"><div className="mx-auto max-w-5xl"><h1 className="text-3xl font-bold text-white">Depth Map Viewer</h1><p className="mt-3 text-slate-400">The default depth provider is an offline-safe pseudo-depth fallback and is not metric depth.</p><DepthMapGallery maps={[]} /></div></main>;
}
