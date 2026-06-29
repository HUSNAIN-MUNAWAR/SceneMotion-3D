import { API_BASE } from '@/lib/api';
export default function ArtifactDownloads({ jobId }: { jobId: string }) {
  const items = [{label:'HTML report', url:`${API_BASE}/api/jobs/${jobId}/report`},{label:'PDF report', url:`${API_BASE}/api/jobs/${jobId}/report?fmt=pdf`},{label:'Sparse cloud PLY', url:`${API_BASE}/api/jobs/${jobId}/pointcloud`},{label:'Dense cloud PLY', url:`${API_BASE}/api/jobs/${jobId}/pointcloud?dense=true`}];
  return <div className="card p-6"><h2 className="font-semibold text-white">Artifacts</h2><div className="mt-3 space-y-2">{items.map(i => <a key={i.label} href={i.url} className="block rounded-lg border border-slate-700 p-3 text-sm text-blue-300 hover:bg-slate-800">{i.label}</a>)}</div></div>;
}
