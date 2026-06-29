import fs from 'fs';
import path from 'path';
const root = path.resolve(process.cwd());
const required = [
  'frontend/package.json',
  'frontend/app/page.tsx',
  'frontend/app/upload/page.tsx',
  'frontend/app/jobs/[jobId]/page.tsx',
  'frontend/components/VideoUpload.tsx',
  'frontend/components/PointCloudViewer.tsx',
  'frontend/lib/api.ts'
];
let ok = true;
for (const rel of required) {
  if (!fs.existsSync(path.join(root, rel))) {
    console.error(`Missing ${rel}`);
    ok = false;
  }
}
const componentDir = path.join(root, 'frontend/components');
for (const file of fs.readdirSync(componentDir).filter(f => f.endsWith('.tsx'))) {
  const text = fs.readFileSync(path.join(componentDir, file), 'utf8');
  if (/dummy|placeholder button/i.test(text)) {
    console.error(`Suspicious dummy UI language in ${file}`);
    ok = false;
  }
}
if (!ok) process.exit(1);
console.log('Frontend static check passed');
