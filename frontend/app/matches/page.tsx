import FeatureMatchViewer from '@/components/FeatureMatchViewer';
export default function MatchViewerPage() {
  return <main className="min-h-screen p-8"><div className="mx-auto max-w-5xl"><h1 className="text-3xl font-bold text-white">Feature Match Viewer</h1><p className="mt-3 text-slate-400">Completed jobs expose match visualization images under their artifact list.</p><FeatureMatchViewer images={[]} /></div></main>;
}
