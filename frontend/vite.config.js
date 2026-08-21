import { defineConfig, loadEnv } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'
import { copyFileSync } from 'fs'
import { emitRoutes } from './vite-plugins/emit-build-data.js'

// This config builds the WEBSITE version only.
// The Capacitor/Android build is not set up for this — don't run
// `npx cap sync` against this output.

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), '')
  const devProxyTarget = env.VITE_DEV_PROXY_TARGET || 'http://127.0.0.1:8000'

  return {
    plugins: [
      vue(),
      emitRoutes({
        routerFile: './src/router/index.js',
        outFile: '../samaaja/vue_routes.json',
        // Only `login` needs listing: Frappe ships frappe/www/login.html,
        // and our Vue login screen takes that address over on purpose.
        // Nothing else in the Vue router collides with a Frappe page --
        // note Frappe has `complete_signup`, not `signup`.
        intentionalOverrides: ['login'],
      }),
      {
        name: 'copy-index-to-www',
        closeBundle() {
          copyFileSync('../samaaja/public/frontend/index.html',
                       '../samaaja/www/index.html')
        }
      }
    ],
    resolve: { alias: { '@': path.resolve(__dirname, './src') } },
    base: '/assets/samaaja/frontend/',
    build: {
      outDir: '../samaaja/public/frontend',
      emptyOutDir: true
    },
    server: {
      proxy: {
        '/api':     { target: devProxyTarget, changeOrigin: true, cookieDomainRewrite: 'localhost' },
        '/files':   { target: devProxyTarget, changeOrigin: true },
        '/private': { target: devProxyTarget, changeOrigin: true }
      }
    }
  }
})
