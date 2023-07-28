import { defineConfig } from 'vite'

export default defineConfig({
  build: {
    sourcemap: true,
    emptyOutDir: false,
    outDir: 'static/js/',
    lib: {
      entry: 'components/index.ts',
      formats: ['iife'],
      name: 'my_components',
      fileName: () => "my_components.min.js",
    },
  }
})
