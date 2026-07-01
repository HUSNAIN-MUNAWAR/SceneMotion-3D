import './globals.css';
import type { Metadata } from 'next';
import type { ReactNode } from 'react';
export const metadata: Metadata = { title: 'SceneMotion 3D', description: 'Monocular visual odometry and 3D reconstruction platform' };
export default function RootLayout({ children }: { children: ReactNode }) {
  return <html lang="en"><body>{children}</body></html>;
}
