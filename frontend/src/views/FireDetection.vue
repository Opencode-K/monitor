<template>
  <div>
    <h2>🔥 火灾检测</h2>
    <a-row :gutter="16">
      <a-col :span="8" v-for="cam in filteredCams" :key="cam.name">
        <MonitorCard
          source="fire"
          :title="cam.name"
          :name="cam.name"
          task="fire"
          :onEdit="() => editMonitor(cam)"
          :onDelete="() => removeMonitor(cam.name)"
          :detectionResults="detectionResults[cam.name] || []"
        />
      </a-col>
    </a-row>
    <!-- <a-card title="检测日志" style="margin-top:24px; max-height:200px; overflow:auto">
      <div v-for="(log,i) in logs" :key="i">{{ log }}</div>
    </a-card> -->
    <AlarmLog task="火灾检测"  />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'
import MonitorCard from '../components/MonitorCard.vue'
import AlarmLog from '../components/AlarmLog.vue'
// console.log(import.meta.env.VITE_API_HOST)

// 全部摄像头列表
const monitors = ref([])
// 本页面日志
const logs = ref([])

// 检测结果，按摄像头名存储
const detectionResults = ref({})

// 只筛选参与“火灾检测”的摄像头
const filteredCams = computed(() =>
  monitors.value.filter(m => m.tasks?.includes('火灾检测'))
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
async function removeMonitor(name) {
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
      detectionResults.value[cam.name] = res.data || []
      res.data
       .filter(r => r.label === 'Fire')
       .forEach(r =>
         logs.value.unshift(`${cam.name} → ${r.label} ${(r.conf * 100).toFixed(1)}%`)
       )
    } catch (e) {
      detectionResults.value[cam.name] = []
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
