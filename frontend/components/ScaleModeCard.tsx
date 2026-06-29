export default function ScaleModeCard() {
  return <div className="rounded-2xl border border-amber-500/40 bg-amber-500/10 p-4 text-sm text-amber-100">
    <b>Why monocular scale is ambiguous:</b> a single moving camera can estimate relative motion, but absolute meters require a scale source such as known distance, known camera height, RGB-D/stereo, IMU, or ground truth for evaluation.
  </div>
}
