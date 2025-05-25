import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path';

export default defineConfig({
  root: path.resolve(__dirname, 'src'), // Укажи корень как src/renderer
  base: "./",
  build: {

    outDir: path.resolve(__dirname, 'dist/src/render'), // куда складывать собранное
    emptyOutDir: true,
  },
  plugins: [
    react(),
  ],
});