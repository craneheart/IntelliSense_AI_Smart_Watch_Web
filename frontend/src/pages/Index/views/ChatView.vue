<script setup>
import VanishingInput from "@/components/input/VanishingInput.vue";
import SparklesText from "@/components/text/SparklesText.vue";
import MultiStepLoader from "@/components/visualization/MultiStepLoader.vue";
import TextGenerateEffect from "@/components/text/TextGenerateEffect.vue";
import deepseek from "@/api/websockets/DeepSeek.js";


import {useRoute} from "vue-router";
import {computed, onMounted, reactive, ref} from "vue";

const placeholders = [
  "我现在的心率是多少?",
  "我要开始1km长跑了,开始记录我的身体状况",
  "读一下这一周我的健康状态分析",
  "请指导我进行深蹲训练",
];

// 消息列表数据
const messages = ref([]);
const isMessage = ref(false);
const chatting = ref(false);
const messageLoading = reactive({
  connection: true,
  send: true,
  processed: true,
});
let currentMessage
let ws
onMounted(() => {
  const route = useRoute()
  const message = route.query.message
  if (message) {
    // 新建消息框,开始调用异步处理
    uploadMessage(message);
  } else {
    // 空白页面
    isMessage.value = false;
  }
})

// async
const loadingMessage = ref(false);
const currentAsyncStep = ref(null);

function uploadMessage(e) {
  if (chatting.value) {
    return;
  }
  currentMessage = e
  loadingMessage.value = true;
  messageLoading.send = true;
  messageLoading.processed = true;
  // 连接到服务器
  if (messageLoading.connection) {
    ws = deepseek().ws;
    ws.onopen = () => {
      messageLoading.connection = false;
    }
    ws.onclose = () => {
      messageLoading.connection = true;
    }
  }

}

const loadingMessageSteps = computed(() => [
      {
        text: "连接到服务器",
        afterText: "连接成功",
        async: messageLoading.connection,
        action: () => {
          sendMessage(currentMessage);
        }
      },
      {
        text: "发送文本消息",
        afterText: "文本发送完毕",//TODO:添加这一段验证
        async: messageLoading.send,
      },
      {
        text: "正在思考",
        afterText: "思考完毕",
        async: messageLoading.processed, // 需要手动触发进入下一步
      },
    ]
)

function sendMessage(message) {
  // 添加用户消息到消息列表
  loadingMessage.value = true;
  messages.value.push({
    id: Date.now(),
    content: message,
    isUser: true,
    timestamp: new Date().toLocaleTimeString()
  });
  isMessage.value = true;
  ws.send(JSON.stringify({
        commend: "signal",
        signal: 'message',
        data: message
      }
  ))
  messageLoading.send = false;
  newAssistantMessage();
}

function newAssistantMessage() {
  const assistantMessage = {
    id: Date.now(),
    content: ['  '],
    isUser: false,
  };
  const messageIndex = messages.value.length;
  messages.value.push(assistantMessage);

  ws.onmessage = event => {
    messageLoading.processed = false;
    // 直接通过索引访问响应式数组中的对象
    messages.value[messageIndex].content.push(event.data);
    console.log()
  };
}


function sendAudio() {
  // 将来实现音频发送功能
  loadingMessage.value = true;

  // 模拟发送音频过程
  setTimeout(() => {
    loadingMessage.value = false;
    receiveMessage();
  }, 2000);
}


function handleComplete() {
  loadingMessage.value = false
}

function handleStateChange(state) {
}
</script>

<template>
  <MultiStepLoader
      :default-duration="100"
      :loading="loadingMessage"
      :prevent-close="true"
      :steps="loadingMessageSteps"
      @close="loadingMessage.value = false"
      @complete="handleComplete"
      @state-change="handleStateChange"
  />
  <div class="flex flex-col items-center justify-center mt-40">
    <SparklesText class="text-xl sm:text-2xl md:text-4xl lg:text-5xl mb-10"
                  text="康聆助手, 随时找我!"/>
    <div id="messageBox"
         class="w-4/5 sm:w-3/4 md:w-2/3 lg:w-1/2 max-h-[60vh] overflow-y-auto flex flex-col gap-4 scroll-smooth  rounded-lg p-4 bg-white/80 shadow-lg">
      <template v-for="(message, index) in messages" :key="message.id">
        <!-- 用户消息 -->
        <div v-if="message.isUser" class="flex justify-end">
          <div class="bg-blue-500 text-white p-3 rounded-lg max-w-[80%]">
            {{ message.content }}
          </div>
        </div>

        <!-- 助手消息 -->
        <div v-else class="flex">
          <div class="bg-gray-200 p-3 rounded-lg max-w-[80%]">
            <template v-for="(words, index) in message.content" :key="index">
              <TextGenerateEffect
                  :duration="0.7"
                  :words="words"
                  class="inline-block mx-0"
              />
            </template>
          </div>
        </div>
      </template>
    </div>
    <VanishingInput :autofocus="true"
                    :placeholders="placeholders"
                    class="mt-10"
                    @submit="uploadMessage"></VanishingInput>
  </div>
</template>

<style scoped>
#messageBox:empty {
  @apply p-0 shadow-none bg-transparent;
}
</style>
