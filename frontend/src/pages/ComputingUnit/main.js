import {createApp} from 'vue'
import App from './App.vue'
import router from './router'
import store from "./store"
import {initTheme} from '@/components/useTheme'
import '@/assets/main.css'

const app = createApp(App)

initTheme()
app.use(router)
app.use(store)
app.mount('#app')
