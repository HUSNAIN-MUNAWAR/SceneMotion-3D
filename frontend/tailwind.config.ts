import type { Config } from 'tailwindcss';
const config: Config = {
  content: ['./app/**/*.{ts,tsx}', './components/**/*.{ts,tsx}'],
  theme: { extend: { boxShadow: { glow: '0 0 50px rgba(59,130,246,0.25)' } } },
  plugins: []
};
export default config;
