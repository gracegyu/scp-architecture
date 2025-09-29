import { defineConfig, searchForWorkspaceRoot } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'node:path'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    fs: {
      // 프로젝트 루트 및 워크스페이스 루트와 외부 dummy/trame 디렉터리 허용
      allow: [
        searchForWorkspaceRoot(process.cwd()),
        '/Users/gracegyu/Documents/Azure/scp-architecture/dummy',
        '/Users/gracegyu/Documents/Azure/scp-architecture/trame-vtklocal',
      ],
    },
  },
})
