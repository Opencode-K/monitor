import { createApp } from 'vue'
import App from './App.vue'
import Antd from 'ant-design-vue'
import 'ant-design-vue/dist/reset.css'
import router from './router'
import './utils/axios'

createApp(App).use(router).use(Antd).mount('#app')

// const app = createApp(App)
// app.use(router)
// app.mount('#app')
