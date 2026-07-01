import { jobBundleUrl, jobPointCloudUrl, jobReportUrl } from '@/lib/api';

export default function ArtifactDownloads({ jobId }: { jobId: string }) {
  const items = [
    { label: 'HTML report', url: jobReportUrl(jobId) },
    { label: 'PDF report', url: jobReportUrl(jobId, 'pdf') },
    { label: 'Sparse cloud PLY', url: jobPointCloudUrl(jobId) },
    { label: 'Dense cloud PLY', url: jobPointCloudUrl(jobId, true) },
    { label: 'Artifact bundle ZIP', url: jobBundleUrl(jobId) },
  ];

  return <div className="card p-6"><h2 className="font-semibold text-white">Artifacts</h2><div className="mt-3 space-y-2">{items.map(item => <a key={item.label} href={item.url} className="block rounded-xl border border-slate-700 bg-slate-950/40 p-3 text-sm text-blue-300 transition hover:border-blue-400 hover:bg-slate-800">{item.label}</a>)}</div></div>;
}
