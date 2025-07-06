<template>
  <div>
    <h2>异常温度</h2>

    <a-row :gutter="16">
      <!-- 这里只循环 filteredCams 而非 monitors -->
      <a-col :span="8" v-for="cam in filteredCams" :key="cam.name">
        <MonitorCard
          source="temp"
          :title="cam.name"
          :name="cam.name"
          task="temp"
          :onEdit="() => editMonitor(cam)"
          :onDelete="() => removeMonitor(cam.name)"
        />
      </a-col>
    </a-row>

    <!-- 日志面板 -->
    <a-card title="检测日志" style="margin-top:24px; max-height:200px; overflow-y:auto">
      <div v-for="(log, idx) in logs" :key="idx">{{ log }}</div>
    </a-card>
    <AlarmLog />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'
import MonitorCard from '../components/MonitorCard.vue'
import AlarmLog from '../components/AlarmLog.vue'

// 全部摄像头列表
const monitors = ref([])
// 本页面日志
const logs = ref([])

// 只筛选参与“烟雾检测”的摄像头
const filteredCams = computed(() =>
  monitors.value.filter(m => m.tasks?.includes('异常温度'))
)

// 拉取摄像头配置
async function fetchMonitors() {
  try {
    const res = await axios.get('/cameras')

    monitors.value = res.data
  } catch (e) {
    console.error('Fetch cameras failed', e)
  }
}

// 删除和编辑用的回调（可复用主页面逻辑）
function editMonitor(cam) {
  // 跳转回主页面或弹窗编辑（按你已有逻辑）
  // 例如：router.push({ name: 'Dashboard', query: { edit: cam.name } })
}
const removeMonitor = async (name) => {
  await axios.delete(`/cameras/${encodeURIComponent(name)}`)
  
  fetchMonitors()
}

// 轮询该页面所有摄像头的检测结果
async function pollResults() {
  for (const cam of filteredCams.value) {
    try {
      const res = await axios.get(
        `/detection/results/${encodeURIComponent(cam.name)}`
      )
      // res.data 是一个数组，可能为空
      res.data
       .filter(r => r.label === 'Temp')
       .forEach(r =>
         logs.value.unshift(`${cam.name} → ${r.label} ${(r.conf * 100).toFixed(1)}%`)
       )
    } catch (e) {
      console.warn(`SmokeDetection poll failed for ${cam.name}`, e)
    }
  }
  // 保留最新 100 条
  if (logs.value.length > 100) logs.value.splice(100)
}

onMounted(async () => {
  await fetchMonitors()
  await pollResults()
  setInterval(pollResults, 2000)
})
</script>
