<script setup>
import TextGenerateEffect from "@/components/text/TextGenerateEffect.vue";
import ExpandableGallery from "@/components/container/ExpandableGallery.vue";
import CardContainer from "@/components/cards/3DCardEffect/CardContainer.vue";
import CardBody from "@/components/cards/3DCardEffect/CardBody.vue";
import CardItem from "@/components/cards/3DCardEffect/CardItem.vue";
import SparklesText from "@/components/text/SparklesText.vue";
import VanishingInput from "@/components/input/VanishingInput.vue";
import FlipCard from "@/components/cards/FlipCard.vue";
import router from '../router/index.js'

const images = [
  "/static/images/realWatch/1.jpg",
  "/static/images/realWatch/2.jpg",
  "/static/images/realWatch/3.jpg",
  "/static/images/realWatch/4.jpg",
  "/static/images/realWatch/5.jpg",
]
const placeholders = [
  "我现在的心率是多少?",
  "我要开始1km长跑了,开始记录我的身体状况",
  "读一下这一周我的健康状态分析",
  "请指导我进行深蹲训练",
];

function switchToChat(e) {
  router.push({
    name: 'chat',
    query: {message: e}
  })
}

</script>

<template>
  <div>
    <div class="mt-20 flex flex-col items-center justify-center">
      <div class="flex flex-col items-center justify-center mt-10">
        <TextGenerateEffect class="text-8xl mb-10" duration="0.7" words="康聆脉动"/>
        <TextGenerateEffect class="text-3xl mb-10" duration="0.7" words="——AI驱动多模态健康监测手环"/>
        <div class="flex flex-col sm:flex-col md:flex-row items-center justify-around w-fit md:w-3/4">
          <FlipCard>
            <template #default>
              <img
                  alt="image"
                  class="size-full rounded-2xl object-cover shadow-2xl shadow-black/40"
                  src="@/assets/images/watchModel/1.png"
              />
              <div class="absolute bottom-4 left-4 text-xl font-bold text-black">自主设计建模</div>
            </template>
            <template #back>
              <div class="flex min-h-full flex-col gap-2">
                <h1 class="text-xl font-bold text-white">自主设计建模</h1>
                <p class="mt-1 border-t border-t-gray-200 py-4 text-base font-medium leading-normal text-gray-100">
                  考虑表壳和表带的获取方法,表壳采用CAD软件solidworks建3D模型用光固化3D打印,表带兼容市场保有量大的苹果表带.
                </p>
              </div>
            </template>
          </FlipCard>
          <ExpandableGallery :images="images" class="w-full sm:w-fit md:w-2/3 lg:w-1/2 xl:w-3/8"/>
          <FlipCard>
            <template #default>
              <img
                  alt="image"
                  class="size-full rounded-2xl object-cover shadow-2xl shadow-black/40"
                  src="@/assets/images/PCB/PCB.png"
              />
              <div class="absolute bottom-1 left-4 text-xl font-bold">PCB开发</div>
            </template>
            <template #back>
              <div class="flex min-h-full flex-col gap-2">
                <h1 class="text-xl font-bold text-white">PCB开发</h1>
                <p class="mt-1 border-t border-t-gray-200 py-4 text-base font-medium leading-normal text-gray-100">
                  为了满足手环应用的特点（集成度高，面积小，轻便，功能多元等），采取PCB设计技术将所需的模块集成在一块小电路板上。
                </p>
              </div>
            </template>
          </FlipCard>
        </div>
      </div>
      <div class="flex flex-col items-center justify-center mt-40">
        <TextGenerateEffect class="text-xl md:text-2xl lg:text-4xl" delay="900" words="集成 三大 开源 AI 模型"/>
        <TextGenerateEffect class="text-2xl md:text-3xl lg:text-5xl" delay="1500"
                            words="Fast-whisper | DeepSeek | Chat-TTS"/>
      </div>
      <div class="flex flex-col lg:flex-row items-center justify-around mt-10">
        <CardContainer>
          <CardBody
              class="group/card relative size-auto rounded-xl border border-black/[0.1] bg-gray-50 p-6 sm:w-[30rem] dark:border-white/[0.2] dark:bg-black dark:hover:shadow-2xl dark:hover:shadow-emerald-500/[0.1]"
          >
            <CardItem :translate-z="50" class="text-xl font-bold text-neutral-600 dark:text-white">
              Fast-whisper
            </CardItem>
            <CardItem as="p"
                      class="mt-2 max-w-sm text-sm text-neutral-500 dark:text-neutral-300"
                      translate-z="60">
              Fast-whisper 是一个快速的语音识别模型，支持多种语言和方言。它可以将语音转换为文本，并且具有较高的准确性和速度。
            </CardItem>
            <CardItem :translate-z="100"
                      class="mt-4 w-full">
              <img
                  alt="Fast-Whisper"
                  class="h-60 w-full rounded-xl object-cover group-hover/card:shadow-xl"
                  height="2253"
                  src="@/assets/images/AIModels/FastWhisper.png"
                  width="2973"
              />
            </CardItem>
            <div class="mt-20 flex items-center justify-between">
              <CardItem
                  :translate-z="20"
                  as="a"
                  class="rounded-xl px-4 py-2 text-xs font-normal dark:text-white"
                  href="https://github.com/SYSTRAN/faster-whisper"
                  target="__blank"
              >
                Visit →
              </CardItem>
              <CardItem
                  :translate-z="20"
                  as="button"
                  class="rounded-xl bg-black px-4 py-2 text-xs font-bold text-white dark:bg-white dark:text-black"
              >
                文档
              </CardItem>
            </div>
          </CardBody>
        </CardContainer>
        <CardContainer>
          <CardBody
              class="group/card relative size-auto rounded-xl border border-black/[0.1] bg-gray-50 p-6 sm:w-[30rem] dark:border-white/[0.2] dark:bg-black dark:hover:shadow-2xl dark:hover:shadow-emerald-500/[0.1]"
          >
            <CardItem :translate-z="50" class="text-xl font-bold text-neutral-600 dark:text-white">
              DeepSeek
            </CardItem>
            <CardItem as="p"
                      class="mt-2 max-w-sm text-sm text-neutral-500 dark:text-neutral-300"
                      translate-z="60">
              DeepSeek是由杭州深度求索人工智能基础技术研究有限公司开发的开源AI大模型，其依托混合专家模型（MoE）、多头潜在注意力（MLA）等先进技术，以低成本、高效率和优秀的中文处理能力著称，支持编程辅助、数学推理、多模态交互等场景
            </CardItem>
            <CardItem :translate-z="100"
                      class="mt-4 w-full">
              <img
                  alt="Fast-Whisper"
                  class="h-60 w-full rounded-xl object-cover group-hover/card:shadow-xl"
                  height="540"
                  src="@/assets/images/AIModels/deepseek.png"
                  width="960"
              />
            </CardItem>
            <div class="mt-20 flex items-center justify-between">
              <CardItem
                  :translate-z="20"
                  as="a"
                  class="rounded-xl px-4 py-2 text-xs font-normal dark:text-white"
                  href="https://chat.deepseek.com/"
                  target="__blank"
              >
                Visit →
              </CardItem>
              <CardItem
                  :translate-z="20"
                  as="button"
                  class="rounded-xl bg-black px-4 py-2 text-xs font-bold text-white dark:bg-white dark:text-black"
              >
                文档
              </CardItem>
            </div>
          </CardBody>
        </CardContainer>
        <CardContainer>
          <CardBody
              class="group/card relative size-auto rounded-xl border border-black/[0.1] bg-gray-50 p-6 sm:w-[30rem] dark:border-white/[0.2] dark:bg-black dark:hover:shadow-2xl dark:hover:shadow-emerald-500/[0.1]"
          >
            <CardItem :translate-z="50" class="text-xl font-bold text-neutral-600 dark:text-white">
              Chat-TTS
            </CardItem>
            <CardItem as="p"
                      class="mt-2 max-w-sm text-sm text-neutral-500 dark:text-neutral-300"
                      translate-z="60">
              Chat-TTS 是一个高效的文本转语音（Text-to-Speech）AI模型，能够将文本内容转换为自然流畅的语音输出，支持多种语言和音色，特别适用于对话场景
            </CardItem>
            <CardItem :translate-z="100"
                      class="mt-4 w-full">
              <img
                  alt="Fast-Whisper"
                  class="h-60 w-full rounded-xl object-cover group-hover/card:shadow-xl"
                  height="660"
                  src="@/assets/images/AIModels/Chat-TTS.png"
                  width="1200"
              />
            </CardItem>
            <div class="mt-20 flex items-center justify-between">
              <CardItem
                  :translate-z="20"
                  as="a"
                  class="rounded-xl px-4 py-2 text-xs font-normal dark:text-white"
                  href="https://www.chattts.co/zh"
                  target="__blank"
              >
                Visit →
              </CardItem>
              <CardItem
                  :translate-z="20"
                  as="button"
                  class="rounded-xl bg-black px-4 py-2 text-xs font-bold text-white dark:bg-white dark:text-black"
              >
                文档
              </CardItem>
            </div>
          </CardBody>
        </CardContainer>
      </div>
      <div class="flex flex-col items-center justify-center mt-40">
        <SparklesText class="text-xl sm:text-2xl md:text-4xl lg:text-5xl mb-10" text="康聆助手, 随时找我!"/>
        <VanishingInput :autofocus="false"
                        :placeholders="placeholders"
                        class="mt-10"
                        @submit="switchToChat"></VanishingInput>
      </div>
    </div>
  </div>
</template>

<style scoped>

</style>