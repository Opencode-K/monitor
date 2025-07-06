<template>
  <a-card title="管理员登录" style="max-width:400px; margin:100px auto;">
    <a-form
      :model="form"
      :rules="rules"
      layout="vertical"
      @finish="onFinish"
    >
      <!-- 用 prop 绑定校验字段 -->
      <a-form-item label="用户名" name="username">
        <a-input
          v-model:value="form.username"
          placeholder="请输入用户名"
        />
      </a-form-item>

      <a-form-item label="密码" name="password">
        <a-input-password
          v-model:value="form.password"
          placeholder="请输入密码"
        />
      </a-form-item>

      <a-form-item>
        <a-button type="primary" html-type="submit" block>
          登录
        </a-button>
        <router-link to="/register" style="float:right; margin-top:8px;">
          去注册
        </router-link>
      </a-form-item>
    </a-form>
  </a-card>
</template>

<script setup>
import { reactive } from 'vue'
import { useRouter } from 'vue-router'
import axios from '@/utils/axios'   // <— 同上

const form = reactive({ username: '', password: '' })
const rules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }]
}

const router = useRouter()
async function onFinish() {
  try {
    const res = await axios.post('/auth/login', {
      username: form.username.trim(),
      password: form.password
    })
    localStorage.setItem('access_token', res.data.access_token)
    router.push('/')
  } catch (e) {
    alert(e.response?.data?.msg || '登录失败')
  }
}
</script>