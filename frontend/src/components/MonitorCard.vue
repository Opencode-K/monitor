<template>
  <a-card :title="title" bordered>
    <template #extra>
      <a-dropdown trigger="click">
        <a-button type="text">︙</a-button>
        <template #overlay>
          <a-menu @click="onMenu">
            <a-menu-item key="edit">修改信息</a-menu-item>
            <a-menu-item key="delete">删除摄像头</a-menu-item>
          </a-menu>
        </template>
      </a-dropdown>
    </template>

    <!-- 画面区域 -->
    <template #cover>
      <div class="monitor-container">
        <!-- 本地/文件视频用 video，其它用 img -->
        <video
          v-if="isVideoFile || type === '本地文件'"
          class="monitor-media"
          :src="videoUrl"
          controls autoplay muted loop
          @error="onVideoError"
        />
        <img
          v-else
          class="monitor-media"
          :src="videoUrl"
          @error="onVideoError"
        />
      </div>
    </template>

    <!-- 检测任务列表或单一任务 -->
    <template #default>
      <div v-if="tasksList.length" class="task-list">
        <a-space wrap>
          <a-tag v-for="task in tasksList" :key="task">{{ task }}</a-tag>
        </a-space>
      </div>
    </template>
  </a-card>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  source: {
    type: String,
    default: 'main'    // main 或 fire/smoke/…
  },
  title: String,
  name: String,
  videoSrc: String,
  type: {
    type: String,
    default: '网络摄像头'
  },
  tasks: {
    type: Array,
    default: () => []
  },
  task: String,
  onEdit: Function,
  onDelete: Function
})

const API_HOST = import.meta.env.VITE_API_HOST || ''
const videoExtRe = /\.(mp4|webm|m3u8)(\?.*)?$/i

// 判断是否为视频文件
const isVideoFile = computed(() => {
  return props.videoSrc && videoExtRe.test(props.videoSrc)
})

// 计算渲染 URL
const videoUrl = computed(() => {
  if (props.source === 'main') { 
    const src = props.videoSrc || ''
    if (isVideoFile.value) {
      return /^https?:\/\//.test(src) ? src : `${API_HOST}${src}`
    }
    if (props.type === '网络摄像头') {
      const base = src.replace(/\/+$/, '')
      return base.endsWith('/stream') ? src : `${base}/stream`
    }
  }
  return `${API_HOST}/api/detection/stream/${encodeURIComponent(props.name)}`
})

// 支持 tasks 数组或单一 task 字符串
const tasksList = computed(() => {
  if (props.tasks && props.tasks.length) return props.tasks
  if (props.task) return [props.task]
  return []
})

function onMenu({ key }) {
  if (key === 'edit') props.onEdit()
  if (key === 'delete') props.onDelete()
}

function onVideoError(e) {
  console.error('Stream error:', e)
}
</script>

<style scoped>
.monitor-container {
  width: 100%;
  height: 200%;
  overflow: hidden;
}
.monitor-media {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
.task-list {
  margin-top: 12px;
}
</style>
