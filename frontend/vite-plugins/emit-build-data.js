import { readFileSync, writeFileSync } from 'fs'

// Reads the router file, pulls out every route address, and writes the
// list where the Python side can read it.
export function emitRoutes({ routerFile, outFile, intentionalOverrides = [] }) {
  return {
    name: 'emit-routes',
    buildStart() {
      const src = readFileSync(routerFile, 'utf8')
      const routes = [...new Set(
        [...src.matchAll(/path:\s*['"]([^'"]+)['"]/g)]
          .map(m => m[1].split('/')[1] || '')
      )]
      writeFileSync(outFile, JSON.stringify({ routes, intentionalOverrides }, null, 2))
      console.log(`[emit-routes] wrote ${routes.length} routes`)
    }
  }
}
