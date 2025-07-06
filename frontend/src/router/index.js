import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'
import Register from '../views/Register.vue'
import Dashboard from '../views/Dashboard.vue'
import FireDetection from '../views/FireDetection.vue'
import SmokeDetection from '../views/SmokeDetection.vue'
import TempDetection from '../views/TempDetection.vue'
import HelmetDetection from '../views/HelmetDetection.vue'

import { ref, computed, onMounted } from 'vue'

const editingName = ref(null)  // 当前正在修改哪个摄像头（用 name 记录）
const isEditing = computed(() => editingName.value !== null)

const routes = [
  { path: '/login', component: Login },
  { path: '/register', component: Register },
  {
    path: '/',
    component: Dashboard,
    meta: { requiresAuth: true }
  },
  {
    path: '/fire',
    component: FireDetection,
    meta: { requiresAuth: true }
  },
  {
    path: '/smoke',
    component: SmokeDetection,
    meta: { requiresAuth: true }
  },
  {
    path: '/temp',
    component: TempDetection,
    meta: { requiresAuth: true }
  },
  {
    path: '/helmet',
    component: HelmetDetection,
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('access_token')
  if (to.meta.requiresAuth && !token) {
    return next('/login')
  }
  next()
})

export default router
