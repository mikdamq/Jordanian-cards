import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import { VitePWA } from 'vite-plugin-pwa';

export default defineConfig({
  base: './',
  plugins: [
    react(),
    VitePWA({
      registerType: 'autoUpdate',
      includeAssets: ['icon.svg', 'apple-touch-icon.png'],
      manifest: {
        name: 'ولا كلمة — Wala Kilmeh',
        short_name: 'ولا كلمة',
        description: 'لعبة تمثيل وتخمين أردنية — Jordanian charades & heads-up party game',
        lang: 'ar',
        dir: 'rtl',
        display: 'standalone',
        orientation: 'any',
        background_color: '#1b1714',
        theme_color: '#1b1714',
        icons: [
          { src: 'icon-192.png', sizes: '192x192', type: 'image/png' },
          { src: 'icon-512.png', sizes: '512x512', type: 'image/png' },
          { src: 'icon-512.png', sizes: '512x512', type: 'image/png', purpose: 'maskable' },
        ],
      },
      workbox: { globPatterns: ['**/*.{js,css,html,svg,png,woff2,wav}'] },
    }),
  ],
});
