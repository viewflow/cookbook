import { defineConfig } from 'vite'

// https://vitejs.dev/config/
export default defineConfig({
  build: {
    outDir: '../../static/client',
  },
  server: {
    proxy: {
      '/api/': 'http://127.0.0.1:8000',
    },
  }
})
