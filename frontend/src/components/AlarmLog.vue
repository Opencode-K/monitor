<template>
  <a-card title="报警日志" style="margin-top:24px; max-height:300px; overflow-y:auto">
    <a-list
      :data-source="displayAlarms"
      bordered
      :locale="{ emptyText: '暂无报警' }"
    >
      <template #renderItem="{ item }">
        <a-list-item :style="{ background: item.ack ? '#f0f0f0' : '#fff' }">
          <a-space direction="vertical" style="width:100%">
            <a-space>
              <a-tag :color="item.ack ? 'default' : 'error'">{{ item.task }}</a-tag>
              <span>{{ item.camera }}</span>
              <span>{{ formatTime(item.time) }}</span>
            </a-space>
            <a-space>
              <span>{{ item.label }} ({{ (item.conf * 100).toFixed(1) }}%)</span>
              <a-button
                v-if="!item.ack"
                type="link"
                size="small"
                @click="ack(item.id)"
              >确认</a-button>
            </a-space>
          </a-space>
        </a-list-item>
      </template>
    </a-list>
  </a-card>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from '@/utils/axios'
import { io } from 'socket.io-client'

const props = defineProps({
  /** 对应后端写入时的 task 字段 */
  task: { type: String, default: '' }
})

const alarms = ref([])

// 计算过滤后的报警列表
const displayAlarms = computed(() => {
  return props.task
    ? alarms.value.filter(a => a.task === props.task)
    : alarms.value
})

// ISO 时间转本地可读格式
function formatTime(iso) {
  const dt = new Date(iso)
  return dt.toLocaleString()
}

async function fetchAlarms() {
  try {
    const res = await axios.get('/detection/alarms')
    alarms.value = res.data
  } catch (e) {
    console.error('拉取报警日志失败', e)
  }
}

// 确认报警
async function ack(id) {
  try {
    await axios.put(`/alarms/${id}/ack`)
    // 标记本地状态
    const alarm = alarms.value.find(a => a.id === id)
    if (alarm) alarm.ack = true
  } catch (e) {
    console.error('确认报警失败', e)
  }
}

onMounted(() => {
  fetchAlarms()
  // 建立 WebSocket 连接，实时接收新报警
  const socket = io(import.meta.env.VITE_API_HOST, { path: '/socket.io' })
  socket.on('new_alarm', alarm => {
    alarms.value.unshift(alarm)
  })
})
</script>

<style scoped>
.a-list-item {
  padding: 8px 16px;
}
</style>
