<script setup>
import {defineEmits, nextTick, onMounted, onUnmounted, ref} from 'vue';
import {realTimeRecognition} from '@/api/websockets/RealTimeRecognition';

// 定义事件
const emit = defineEmits(['recordingStatus', 'recognitionResult']);

// 按钮状态
const isActive = ref(false);
// 音频相关
const audioContext = ref(null);
const analyser = ref(null);
const dataArray = ref([]);
const animationId = ref(null);
const canvasRef = ref(null);
const containerRef = ref(null);
// 录音相关
const processor = ref(null);
const wsConnection = ref(null);
const mediaStream = ref(null);
// 错误状态
const hasError = ref(false);
const errorMessage = ref('');
// 服务器状态
const serverReady = ref(false);

const SAMPLE_RATE = 16000; // 采样率，与服务器端模型匹配
const BUFFER_SIZE = 4096;  // 确保缓冲区大小是4的倍数

// 检查浏览器是否支持所需的API
const checkBrowserCompatibility = () => {
  if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
    return {
      compatible: false,
      message: '您的浏览器不支持麦克风访问。请使用Chrome、Firefox、Safari或Edge的最新版本。'
    };
  }

  if (!window.AudioContext && !window.webkitAudioContext) {
    return {
      compatible: false,
      message: '您的浏览器不支持音频处理功能。请使用Chrome、Firefox、Safari或Edge的最新版本。'
    };
  }

  return {compatible: true};
};

// 按钮点击处理
const toggleRecording = async () => {
  if (isActive.value) {
    stopRecording();
  } else {
    // 检查浏览器兼容性
    const compatibility = checkBrowserCompatibility();
    if (!compatibility.compatible) {
      errorMessage.value = compatibility.message;
      hasError.value = true;
      emit('recordingStatus', compatibility.message);
      return;
    }

    await startRecording();
  }
};

// 处理麦克���错误
const handleMicrophoneError = (err) => {
  if (err.name === 'NotAllowedError' || err.name === 'PermissionDeniedError') {
    errorMessage.value = '麦克风访问被拒绝。请在浏览器设置中允许访问麦克风，并刷新页面。';
  } else if (err.name === 'NotFoundError' || err.name === 'DevicesNotFoundError') {
    errorMessage.value = '未检测到麦克风设备。请确认您的麦克风已正确连接。';
  } else {
    errorMessage.value = `麦克风访问失败: ${err.message}`;
  }
  hasError.value = true;
  emit('recordingStatus', errorMessage.value);

  // 确保关闭WebSocket连接
  if (wsConnection.value) {
    wsConnection.value.closeConnection();
    wsConnection.value = null;
  }
  isActive.value = false;
};

// 浮点音频数据转换为二进制 - 已不再使用，保留供参考
const floatTo16BitPCM = (input) => {
  const output = new Int16Array(input.length);
  for (let i = 0; i < input.length; i++) {
    const s = Math.max(-1, Math.min(1, input[i]));
    output[i] = s < 0 ? s * 0x8000 : s * 0x7FFF;
  }
  return output;
};

// 实际开始录音和分析（在服务器准备就绪后调用）
const startActualRecording = () => {
  if (!mediaStream.value || !serverReady.value) return;

  try {
    emit('recordingStatus', '请讲话...');

    audioContext.value = new (window.AudioContext || window.webkitAudioContext)({
      sampleRate: SAMPLE_RATE
    });

    // 创建音频分析器 - 用于可视化
    analyser.value = audioContext.value.createAnalyser();
    analyser.value.fftSize = 256;

    // 从麦克风创建音频源
    const source = audioContext.value.createMediaStreamSource(mediaStream.value);

    // 创建音频处理节点
    processor.value = audioContext.value.createScriptProcessor(BUFFER_SIZE, 1, 1);

    // 音频处理回调 - 当有新音频数据可用时
    processor.value.onaudioprocess = (audioProcessingEvent) => {
      if (!wsConnection.value || !isActive.value) return;

      // 获取输入音频数据
      const inputData = audioProcessingEvent.inputBuffer.getChannelData(0);

      // 直接发送浮点音频数据，不再转换为16位PCM
      // 后端需要以Float32格式解析这些数据
      try {
        // 创建一个拷贝，因为inputData是只读的
        const floatData = new Float32Array(inputData);
        wsConnection.value.sendAudioData(floatData.buffer);
      } catch (err) {
        console.error('发送音频数据时出错:', err);
      }
    };

    // 连接音频节点
    source.connect(analyser.value);
    analyser.value.connect(processor.value);
    processor.value.connect(audioContext.value.destination);

    // 准备可视化数据数组
    dataArray.value = new Uint8Array(analyser.value.frequencyBinCount);

    // 开始绘制波形
    drawWaveform();

  } catch (err) {
    console.error('开始录音失败:', err);
    emit('recordingStatus', `录音初始化失败: ${err.message}`);
    stopRecording();
  }
};

// 尝试录音和分析
const startRecording = async () => {
  try {
    emit('recordingStatus', '正在请求麦克风权限...');
    hasError.value = false;
    serverReady.value = false;

    // 先获取麦克风权限
    let stream;
    try {
      stream = await navigator.mediaDevices.getUserMedia({
        audio: {
          channelCount: 1,
          sampleRate: SAMPLE_RATE
        },
        video: false
      });
      mediaStream.value = stream;
    } catch (err) {
      handleMicrophoneError(err);
      return;
    }

    // 设置按钮为激���状态
    isActive.value = true;
    emit('recordingStatus', '正在等待服务器准备...');

    // 初始化WebSocket连接
    try {
      // 传入回调函数，在收到服务器ready信号时开始录音
      wsConnection.value = realTimeRecognition(async (readyData) => {
        await wsConnection.value.ws.send(JSON.stringify(
            {
              commend: 'switch_state',
              state: 'voice',
            }
        ))
        console.log('服务器准备就绪:', readyData);
        serverReady.value = true;
        startActualRecording();
        // ws发送状态变化,然后开始接受数据
        wsConnection.value.ws.onmessage = event => {
          const data = JSON.parse(event.data);
          if (data.type === 'recognitionResult') {
            // 处理识别结果
            emit('recognitionResult', data.result);
          } else if (data.type === 'error') {
            console.error('服务器错误:', data.message);
            emit('recordingStatus', `服务器错误: ${data.message}`);
            stopRecording();
          }
        }

      });


      wsConnection.value.ws.onerror = (error) => {
        console.error('WebSocket连接错误:', error);
        emit('recordingStatus', '服务器连接错误，请重试');
        stopRecording();
      };
    } catch (wsError) {
      console.error('WebSocket初始化失败:', wsError);
      emit('recordingStatus', '无法连接到语音识别服务，请检查网络连接');
      stopRecording();
      return;
    }
  } catch (err) {
    console.error('初始化失败:', err);
    errorMessage.value = `初始化失败: ${err.message}`;
    hasError.value = true;
    emit('recordingStatus', errorMessage.value);
    isActive.value = false;
  }
};

// 停止录音
const stopRecording = () => {
  emit('recordingStatus', '已停止');
  isActive.value = false;
  serverReady.value = false;

  // 断开并清理ScriptProcessor
  if (processor.value && audioContext.value) {
    processor.value.disconnect();
    processor.value = null;
  }

  // 确保释放麦克风资源
  if (mediaStream.value) {
    mediaStream.value.getTracks().forEach(track => track.stop());
    mediaStream.value = null;
  }

  if (audioContext.value) {
    audioContext.value.close().catch(err => console.error('关闭音频上下文时出错:', err));
    audioContext.value = null;
  }

  if (animationId.value) {
    cancelAnimationFrame(animationId.value);
    animationId.value = null;
  }

  // 关闭WebSocket连接
  if (wsConnection.value) {
    wsConnection.value.closeConnection();
    wsConnection.value = null;
  }

  // 清除波形
  const canvas = canvasRef.value;
  if (canvas) {
    const ctx = canvas.getContext('2d');
    ctx.clearRect(0, 0, canvas.width, canvas.height);
  }
};

// 绘制声波波形
const drawWaveform = () => {
  if (!analyser.value) return;

  animationId.value = requestAnimationFrame(drawWaveform);

  const canvas = canvasRef.value;
  const ctx = canvas.getContext('2d');
  const width = canvas.width;
  const height = canvas.height;

  // 清除画布
  ctx.clearRect(0, 0, width, height);

  // 获取音频数据
  analyser.value.getByteFrequencyData(dataArray.value);

  // 设置圆形波形
  const centerX = width / 2;
  const centerY = height / 2;
  const radius = Math.min(centerX, centerY) - 50; // 给内部按钮留出空间

  // 只使用前30%的数据
  const dataUsagePercentage = 0.3;
  const dataPointsToUse = Math.floor(dataArray.value.length * dataUsagePercentage);

  // 准备点的坐标数组
  const points = [];
  for (let i = 0; i < 360; i++) {
    const angle = (i / 360) * Math.PI * 2;

    // 将角度映射到前30%的数据点
    const dataIndex = Math.floor((i / 360) * dataPointsToUse);
    const amplitude = dataArray.value[dataIndex] / 255;
    const waveRadius = radius + amplitude * 35;

    const x = centerX + waveRadius * Math.cos(angle);
    const y = centerY + waveRadius * Math.sin(angle);

    points.push({x, y});
  }

  // 绘制平滑曲线
  ctx.beginPath();
  ctx.moveTo(points[0].x, points[0].y);

  // 使用贝塞尔曲线连接点
  for (let i = 0; i < points.length - 1; i++) {
    const current = points[i];
    const next = points[i + 1];

    // 计算控制点（简单的方法是取中点）
    const xc = (current.x + next.x) / 2;
    const yc = (current.y + next.y) / 2;

    // 绘制二次贝塞尔曲线
    ctx.quadraticCurveTo(current.x, current.y, xc, yc);
  }

  // 闭合曲线 - 连接最后一点和第一点
  const last = points[points.length - 1];
  const first = points[0];
  const xc = (last.x + first.x) / 2;
  const yc = (last.y + first.y) / 2;
  ctx.quadraticCurveTo(last.x, last.y, xc, yc);
  ctx.quadraticCurveTo(xc, yc, first.x, first.y);

  ctx.closePath();
  ctx.strokeStyle = isActive.value ? '#000000' : '#666666';
  ctx.lineWidth = 2;
  ctx.stroke();
};

// 调整canvas尺寸
const resizeCanvas = () => {
  if (canvasRef.value && containerRef.value) {
    const container = containerRef.value;
    canvasRef.value.width = container.offsetWidth;
    canvasRef.value.height = container.offsetHeight;
  }
};

// 组件挂载时初始化canvas
onMounted(() => {
  nextTick(() => {
    resizeCanvas();
    window.addEventListener('resize', resizeCanvas);

    // 检查浏览器兼容性并显示初始状态
    const compatibility = checkBrowserCompatibility();
    if (!compatibility.compatible) {
      errorMessage.value = compatibility.message;
      hasError.value = true;
      emit('recordingStatus', compatibility.message);
    } else {
      emit('recordingStatus', '准备就绪，点击按钮开始');
    }
  });
});

// 组件卸载时清理
onUnmounted(() => {
  stopRecording();
  window.removeEventListener('resize', resizeCanvas);
});
</script>

<template>
  <div ref="containerRef" class="relative w-64 h-64">
    <canvas ref="canvasRef" class="absolute top-0 left-0 w-full h-full"></canvas>
    <button
        :class="[
        'absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2',
        'w-24 h-24 rounded-full flex items-center justify-center z-10 transition-all duration-300',
        hasError
          ? 'bg-red-500 text-white shadow-lg'
          : isActive
            ? serverReady ? 'bg-black text-white shadow-lg' : 'bg-yellow-500 text-white shadow-lg'
            : 'bg-white text-black border-2 border-black'
      ]"
        :disabled="hasError"
        aria-label="语音录制按钮"
        @click="toggleRecording"
    >
      <span v-if="hasError">错误</span>
      <span v-else-if="!isActive">启动</span>
      <span v-else-if="isActive && !serverReady">等待</span>
      <span v-else>停止</span>
    </button>
    <div v-if="hasError" class="absolute bottom-0 left-0 w-full text-center text-red-500 text-sm px-2">
      {{ errorMessage }}
    </div>
  </div>
</template>

<style scoped>
/* Tailwind 已经提供了所需的大部分样式 */
</style>

