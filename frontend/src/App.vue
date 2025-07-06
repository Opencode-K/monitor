<template>
  <a-layout style="min-height: 100vh">
    <a-layout-sider collapsible>
      <div class="logo">监控系统</div>
      <a-menu
        theme="dark"
        mode="inline"
        :selectedKeys="[route.path]"
         @click="handleMenuClick"
      >
        <a-menu-item key="/">
          <router-link to="/" class="menu-link">主界面</router-link>
        </a-menu-item>
        <a-menu-item key="/fire">
          <router-link to="/fire" class="menu-link">火灾检测</router-link>
        </a-menu-item>
        <a-menu-item key="/smoke">
          <router-link to="/smoke" class="menu-link">烟雾检测</router-link>
        </a-menu-item>
        <a-menu-item key="/temp">
          <router-link to="/temp" class="menu-link">异常温度</router-link>
        </a-menu-item>
        <a-menu-item key="/helmet">
          <router-link to="/helmet" class="menu-link">人员佩戴</router-link>
        </a-menu-item>
      </a-menu>
    </a-layout-sider>

    <a-layout>
      <a-layout-header style="background: white; padding: 0 24px; font-size: 18px">
        多任务监控显示系统
      </a-layout-header>
      <a-layout-content style="margin: 24px">
        <router-view :key="$route.fullPath" />
      </a-layout-content>
    </a-layout>
  </a-layout>
</template>

<script setup>
import { useRoute } from 'vue-router'
const route = useRoute()
// 点击菜单跳转
function handleMenuClick({ key }) {
  if (key !== currentRoute) {
    router.push(key)
  }
}
</script>

<style scoped>
.logo {
  height: 60px;
  color: white;
  font-size: 20px;
  padding: 20px 0 12px 24px;
  font-weight: bold;
}

/* 菜单项内的 <router-link> 全宽覆盖，去掉默认 a 标签样式 */
.menu-link {
  display: block;
  color: inherit;
  text-decoration: none;
}

/* 调整菜单项间距和高度 */
::v-deep(.ant-menu-item) {
  margin-bottom: 12px !important;
  height: 48px !important;
  line-height: 48px !important;
  font-size: 16px;
  padding-left: 24px !important;
}

/* 选中项圆角高亮 */
::v-deep(.ant-menu-item-selected) {
  border-radius: 8px;
}
</style>
