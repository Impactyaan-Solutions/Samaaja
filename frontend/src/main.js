import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import router from './router'
import i18n from './i18n'

const app = createApp(App)
app.use(router)
app.use(i18n)
// Apply theme color from backend
function applyThemeColor(hex) {
  if (!hex) return

  document.documentElement.style.setProperty('--color-primary', hex)
}
const themeColor = window.__APP_COLOUR__
if (themeColor) {
  applyThemeColor(themeColor)
}

app.mount('#app')
