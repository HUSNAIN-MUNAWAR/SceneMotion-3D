import './globals.css';
import type { Metadata } from 'next';
export const metadata: Metadata = { title: 'SceneMotion 3D', description: 'Monocular visual odometry and 3D reconstruction platform' };
export default function RootLayout({ children }: { children: React.ReactNode }) {
  return <html lang="en"><body>{children}</body></html>;
}
