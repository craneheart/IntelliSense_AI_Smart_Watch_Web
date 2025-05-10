<script setup>
import {onMounted, ref, watch} from 'vue'
import * as pdfjsLib from 'pdfjs-dist'

// 定义组件的 props
const props = defineProps({
  url: {
    type: String,
    default: ''
  }
})

pdfjsLib.GlobalWorkerOptions.workerSrc = new URL(
    'pdfjs-dist/build/pdf.worker.mjs',
    import.meta.url
).toString()

const pdfDoc = ref(null)
const pageNum = ref(1)
const pageCount = ref(0)
const canvasRef = ref(null)
const loading = ref(false)
const error = ref('')

async function loadPdf(url) {
  if (!url) return

  loading.value = true
  error.value = ''
  try {
    pdfDoc.value = await pdfjsLib.getDocument(url).promise
    pageCount.value = pdfDoc.value.numPages
    pageNum.value = 1
    await renderPage(pageNum.value)
  } catch (e) {
    error.value = '加载PDF失败'
  }
  loading.value = false
}

async function renderPage(num) {
  if (!pdfDoc.value) return
  const page = await pdfDoc.value.getPage(num)
  const viewport = page.getViewport({scale: 1.5})
  const canvas = canvasRef.value
  const context = canvas.getContext('2d')
  canvas.height = viewport.height
  canvas.width = viewport.width
  await page.render({canvasContext: context, viewport}).promise
}

function prevPage() {
  if (pageNum.value <= 1) return
  pageNum.value--
  renderPage(pageNum.value)
}

function nextPage() {
  if (pageNum.value >= pageCount.value) return
  pageNum.value++
  renderPage(pageNum.value)
}

// 监听 url 属性的变化
watch(() => props.url, (newUrl) => {
  if (newUrl) {
    loadPdf(newUrl)
  } else {
    // URL 为假值时清除当前显示
    pdfDoc.value = null
    pageCount.value = 0
  }
}, {immediate: true})

onMounted(() => {
  // 如果初始有 URL，则加载 PDF
  if (props.url) {
    loadPdf(props.url)
  }
})
</script>

<template>
  <div class="flex flex-col items-center w-full">
    <div v-if="error" class="text-red-500 mb-2">{{ error }}</div>

    <!-- 当 URL 为假值或正在加载时显示加载状态 -->
    <div v-if="!props.url || loading" class="text-gray-500">加载中...</div>

    <div v-else-if="pdfDoc">
      <canvas ref="canvasRef" class="border border-gray-300 max-w-full mb-2 rounded shadow"/>
      <div v-if="pageCount > 0" class="flex items-center justify-center space-x-4 mt-2">
        <button
            :disabled="pageNum<=1"
            class="px-4 py-1 rounded bg-blue-500 text-white disabled:bg-gray-300 transition"
            @click="prevPage"
        >
          上一页
        </button>
        <span class="text-gray-700">第 {{ pageNum }} / {{ pageCount }} 页</span>
        <button
            :disabled="pageNum>=pageCount"
            class="px-4 py-1 rounded bg-blue-500 text-white disabled:bg-gray-300 transition"
            @click="nextPage"
        >
          下一页
        </button>
      </div>
    </div>
  </div>
</template>
