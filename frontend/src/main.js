import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import router from './router'
import i18n from './i18n'
import { loadBranding } from './branding'

const app = createApp(App)
app.use(router)
app.use(i18n)
loadBranding()

app.mount('#app')
