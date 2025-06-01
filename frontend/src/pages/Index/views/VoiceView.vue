<script setup>
import {computed, ref} from 'vue';
import VoiceButton from '@/components/button/VoiceBotton.vue';
import LineShadowText from "@/components/text/LineShadowText.vue";
import {useTheme} from "@/ulits/useTheme.js"
import TextGenerateEffect from "@/components/text/TextGenerateEffect.vue";
import router from '../router/index.js'

const isDark = computed(() => useTheme().isDark);
const shadowColor = computed(() => (isDark.value ? "black" : "white"));
const recordingStatus = ref('准备就绪');
const recognitionResults = ref([]);
const isRecording = ref(false);

// 当前展示的文本索引
const currentTextIndex = ref(0);
// 是否正在展示文本
const isShowingText = ref(false);
const textDisplay = [
  {text: "智", time: "150"},
  {text: "音", time: "400"},
  {text: "助手", time: "50"},
  {text: "，", time: "300"},
  {text: "请你", time: "600"},
  {text: "分析一下", time: "500"},
  {text: "我当前", time: "150"},
  {text: "的", time: "200"},
  {text: "身体", time: "300"},
  {text: "状况", time: "350"},
]

function textGenerate(index) {
  if (index >= textDisplay.length) {
  } else {
    recognitionResults.value.push(textDisplay[index].text);
    setTimeout(() => {
      textGenerate(index + 1);
    }, textDisplay[index].time);
  }
}

// 处理录音状态更新
const handleRecordingStatus = (status) => {
  recordingStatus.value = status;

  // 根据状态更新录音标志
  if (status === '请讲话...') {
    isRecording.value = true;
    // 清空之前的识别结果，只在开始录音时清空
    recognitionResults.value = [];
    setTimeout(() => {
      textGenerate(0)

    }, 1000)
  } else if (status === '已停止') {
    isRecording.value = false;
    setTimeout(() => {
      router.push({
        name: 'chat',
        query: {message: "康聆助手,请你分析一下我当前的身体状况"}
      })

    }, 2000)
  }
};

// 处理实时识别结果
const handleRecognitionResult = (result) => {
  if (!result || !result.text) return;

  // 如果是临时结果，更新最后一个结果
  if (result.isFinal === false) {
    if (recognitionResults.value.length > 0) {
      recognitionResults.value[recognitionResults.value.length - 1] = result.text;
    } else {
      recognitionResults.value.push(result.text);
    }
  }
  // 如果是最终结果，添加新条目
  else {
    recognitionResults.value.push(result.text);
  }
};

// 清除演示功能，专注于实际语音识别
</script>

<template>
  <div class="flex flex-col items-center justify-center mt-20">
    <div class="flex">
      <h1 class="text-balance text-8xl font-extrabold leading-none tracking-tighter mr-0">用说的,更</h1>
      <h1 class="text-balance text-8xl font-extrabold leading-none tracking-tighter ml-0">
        <LineShadowText :shadow-color="shadowColor" class="italic">轻</LineShadowText>
        <LineShadowText :shadow-color="shadowColor" class="italic">松</LineShadowText>
      </h1>
    </div>
    <div class="p-6 max-w-lg mx-auto">
      <div class="flex flex-col items-center mb-8">
        <VoiceButton
            @recording-status="handleRecordingStatus"
            @recognition-result="handleRecognitionResult"
        />
        <p class="mt-4 text-gray-600">点击中间按钮开始/停止语音识别</p>
      </div>

      <div class="bg-gray-100 dark:bg-gray-700 p-4 rounded-lg">
        <p class="mb-2 dark:text-gray-200">
          <strong>状态:</strong> {{ recordingStatus }}
        </p>
      </div>
    </div>
    <div id="generateText"
         class="w-3/4 flex flex-row items-start mt-8 bg-gray-50 dark:bg-gray-800 p-4 rounded-lg min-h-32">
      <div v-if="recognitionResults.length === 0" class="text-gray-500 dark:text-gray-400 text-center w-full">
        请点击上方按钮
      </div>
      <div v-for="(text, index) in recognitionResults" v-else :key="index" class="flex items-center mb-2">
        <TextGenerateEffect
            :words="text"
            class="text-lg font-medium text-gray-800 dark:text-gray-200 inline-block"
        />
      </div>
    </div>
  </div>
</template>