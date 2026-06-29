export default function DocsPage() {
  return <main className="min-h-screen p-8"><article className="card mx-auto max-w-4xl p-8">
    <h1 className="text-3xl font-bold text-white">Limitations</h1>
    <p className="mt-4 text-slate-300">SceneMotion 3D estimates relative monocular trajectory only. Absolute metric scale needs extra information such as known object size, stereo baseline, IMU, depth sensor, or external scale reference.</p>
    <ul className="mt-6 list-disc space-y-2 pl-6 text-slate-300">
      <li>Low texture and motion blur reduce keypoints.</li>
      <li>Pure rotation and low parallax break triangulation.</li>
      <li>Dynamic objects can corrupt matching.</li>
      <li>Approximate intrinsics reduce geometric accuracy.</li>
      <li>Fallback depth is pseudo-depth for demo use, not metric depth.</li>
    </ul>
  </article></main>;
}
