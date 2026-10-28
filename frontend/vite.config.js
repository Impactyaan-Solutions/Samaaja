import { defineConfig, loadEnv } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'
import { readFileSync, writeFileSync } from 'fs'
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
        writeBundle() {
          let html = readFileSync('../samaaja/public/frontend/index.html', 'utf8')

          // Hand the page's own CSRF token to the app.
          //
          // Frappe renders www/*.html through Jinja before serving, so the
          // expression below is replaced with the real token per request.
          // The app needs it because it is now served by the same site it
          // calls: the session cookie travels with every request, so Frappe
          // rejects writes that arrive without a matching token.
          //
          // It is injected here rather than written into index.html because
          // Vite regenerates that file on every build.
          const csrf = '<script>window.csrf_token = "{{ frappe.session.csrf_token }}";</scr' + 'ipt>'
          html = html.replace('</head>', `  ${csrf}\n  </head>`)

          writeFileSync('../samaaja/www/index.html', html)
          console.log('[copy-index-to-www] wrote www/index.html with csrf token')
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
