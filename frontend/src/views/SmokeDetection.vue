<template>
  <div>
    <h2>🚭 烟雾检测</h2>
    <a-row :gutter="16">
      <a-col :span="8" v-for="cam in filteredCams" :key="cam.name">
        <MonitorCard
          source="smoke"
          :title="cam.name"
          :name="cam.name"
          task="smoke"
          :onEdit="() => editMonitor(cam)"
          :onDelete="() => removeMonitor(cam.name)"
        />
      </a-col>
    </a-row>
    <a-card title="检测日志" style="margin-top:24px; max-height:200px; overflow:auto">
      <div v-for="(log,i) in logs" :key="i">{{ log }}</div>
    </a-card>
    <AlarmLog />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'
import MonitorCard from '../components/MonitorCard.vue'
import AlarmLog from '../components/AlarmLog.vue'

const monitors = ref([]), logs = ref([])

const filteredCams = computed(() =>
  monitors.value.filter(m => m.tasks?.includes('烟雾检测'))
)

async function fetchMonitors(){ monitors.value = (await axios.get('/cameras')).data }

async function pollResults(){
  for(const cam of filteredCams.value){
    try {
      const res = await axios.get(    
        `/detection/results/${encodeURIComponent(cam.name)}`
      )
      res.data
       .filter(r => r.label === 'Smoke')
       .forEach(r =>
         logs.value.unshift(`${cam.name} → ${r.label} ${(r.conf * 100).toFixed(1)}%`)
       )
    } catch(e){}
  }
  logs.value.splice(100)
}

onMounted(async()=>{
  await fetchMonitors()
  pollResults()
  setInterval(pollResults,2000)
})
</script>
