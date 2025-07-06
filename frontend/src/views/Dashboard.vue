

<template>
  <div>
    <h2> 管理主页面</h2>

    <!-- 添加摄像头按钮 -->
    <a-button type="primary" @click="showModal = true" style="margin-bottom: 20px;">添加摄像头</a-button>

    <!-- 添加摄像头弹窗 -->
    <a-modal
      v-model:open="showModal"
      title="添加摄像头"
      @ok="handleSubmitCamera"
      @cancel="resetForm"
      ok-text="添加"
      cancel-text="取消"
    >
      <a-form layout="vertical">
        <a-form-item label="摄像头名称">
          <a-input v-model:value="form.name" placeholder="如：摄像头 A" />
        </a-form-item>

        <a-form-item label="视频流地址">
          <a-input v-model:value="form.video" placeholder="如：http://... 或 /video/xxx.mp4" />
        </a-form-item>

        <a-form-item label="摄像头类型">
          <a-select v-model:value="form.type" placeholder="请选择类型">
            <a-select-option value="本地文件">本地文件</a-select-option>
            <a-select-option value="网络摄像头">网络摄像头</a-select-option>
            <a-select-option value="RTSP流">RTSP流</a-select-option>
          </a-select>
        </a-form-item>

        <a-form-item label="参与检测任务">
          <a-select
            v-model:value="form.tasks"
            mode="multiple"
            placeholder="选择参与的任务"
          >
            <a-select-option value="火灾检测">火灾检测</a-select-option>
            <a-select-option value="烟雾检测">烟雾检测</a-select-option>
            <a-select-option value="异常温度">异常温度</a-select-option>
            <a-select-option value="人员佩戴">人员佩戴</a-select-option>
          </a-select>
        </a-form-item>
      </a-form>
    </a-modal>

    <!-- 摄像头显示区 -->
    <a-row :gutter="16">
     <a-col :span="8" v-for="cam in monitors" :key="cam.name">
      <MonitorCard
        source="main"
        :title="cam.name"
        :name="cam.name"
        :videoSrc="cam.video"
        :tasks="cam.tasks"
        :onEdit="() => editMonitor(cam)"
        :onDelete="() => removeMonitor(cam.name)"
        />
     </a-col>
   </a-row>
   <AlarmLog />
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'
import MonitorCard from '../components/MonitorCard.vue'
import AlarmLog from '../components/AlarmLog.vue'

const monitors = ref([])

const showModal = ref(false)
const form = ref({
  name: '',
  video: '',
  type: '',
  tasks: []
})

const editingName = ref(null)
const isEditing = computed(() => editingName.value !== null)

// 获取摄像头列表
const fetchMonitors = async () => {
  // const res = await axios.get('/cameras')
  const res = await axios.get('/cameras')
  monitors.value = res.data
}

// 提交摄像头（添加或修改）
const handleSubmitCamera = async () => {
  if (!form.value.name || !form.value.video) {
    return alert('请填写摄像头名称和视频地址')
  }

  if (isEditing.value) {
    await axios.put(`/cameras/${encodeURIComponent(editingName.value)}`, form.value)
  } else {
    await axios.post('/cameras', form.value)
  }

  resetForm()
  fetchMonitors()
}

// 编辑摄像头
const editMonitor = (monitor) => {
  form.value = {
    name: monitor.name,
    video: monitor.video,
    type: monitor.type,
    tasks: monitor.tasks
  }
  editingName.value = monitor.name
  showModal.value = true
}

// 删除摄像头
const removeMonitor = async (name) => {
  await axios.delete(`/cameras/${encodeURIComponent(name)}`)
  // await axios.delete('/cameras/${encodeURIComponent(name)}')
  fetchMonitors()
}

// 重置弹窗表单
const resetForm = () => {
  showModal.value = false
  form.value = {
    name: '',
    video: '',
    type: '',
    tasks: []
  }
  editingName.value = null
}

onMounted(fetchMonitors)
</script>
