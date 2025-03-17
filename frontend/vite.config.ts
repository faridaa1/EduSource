import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'node:path'

// https://vite.dev/config/
export default defineConfig((({mode}) => ({
  plugins: [
    vue(),
  ],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src')
    },
  },
  build: {
    emptyOutDir: true,
    outDir: '../api/static/api',
  },
  // base: mode === 'development' ? 'http://localhost:5173/' : '/static/api/' 
  base: mode === 'development' ? 'http://localhost:5173/' : '/' 
})))
