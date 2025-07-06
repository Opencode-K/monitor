<template>
  <a-card title="管理员注册" style="max-width:400px; margin:100px auto;">
    <a-form
      :model="form"
      :rules="rules"
      layout="vertical"
      @finish="onFinish"
    >
      <!-- 注意这里用 prop 而不是 name -->
      <a-form-item label="用户名" name="username">
        <a-input
          v-model:value="form.username"
          placeholder="3–20 位字母数字下划线"
        />
      </a-form-item>

      <a-form-item label="密码" name="password">
        <a-input-password
          v-model:value="form.password"
          placeholder="至少6位，包含字母和数字"
        />
      </a-form-item>

      <a-form-item>
        <a-button type="primary" html-type="submit" block>
          注册
        </a-button>
        <router-link to="/login" style="float: right; margin-top: 8px;">
          去登录
        </router-link>
      </a-form-item>
    </a-form>
  </a-card>
</template>

<script setup>
import { reactive } from 'vue'
import { useRouter } from 'vue-router'
import axios from '@/utils/axios'   // <— 引用我们上面定义的 axios 实例

const form = reactive({
  username: '',
  password: ''
})

const rules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, message: '用户名至少 3 位', trigger: 'blur' },
    { max: 20, message: '用户名最多 20 位', trigger: 'blur' },
    {
      pattern: /^[A-Za-z0-9_]+$/,
      message: '用户名只能包含字母、数字和下划线',
      trigger: 'blur'
    }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码至少 6 位', trigger: 'blur' },
    {
      pattern: /(?=.*[0-9])(?=.*[A-Za-z]).*$/,
      message: '密码需包含字母和数字',
      trigger: 'blur'
    }
  ]
}

const router = useRouter()

async function onFinish() {
  try {
    await axios.post('/auth/register', {
      username: form.username.trim(),
      password: form.password
    })
    alert('注册成功，请登录')
    router.push('/login')
  } catch (e) {
    alert(e.response?.data?.msg || '注册失败')
  }
}
</script>