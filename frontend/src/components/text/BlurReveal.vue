<template>
  <div
      ref="container"
      :class="props.class"
  >
    <Motion
        v-for="(child, index) in children"
        :key="index"
        ref="childElements"
        :in-view="getAnimate()"
        :initial="getInitial()"
        :transition="{
        duration: props.duration,
        easing: 'easeInOut',
        delay: props.delay * index,
      }"
        as="div"
    >
      <component :is="child"/>
    </Motion>
  </div>
</template>

<script lang="ts" setup>
import {Motion} from "motion-v";
import {onMounted, ref, useSlots, watchEffect} from "vue";

interface Props {
  duration?: number;
  delay?: number;
  blur?: string;
  yOffset?: number;
  class?: string;
}

const props = withDefaults(defineProps<Props>(), {
  duration: 1,
  delay: 2,
  blur: "20px",
  yOffset: 20,
});

const container = ref(null);
const childElements = ref([]);
const slots = useSlots();

// eslint-disable-next-line @typescript-eslint/no-explicit-any
const children = ref<any>([]);

onMounted(() => {
  // This will reactively capture all content provided in the default slot
  watchEffect(() => {
    children.value = slots.default ? slots.default() : [];
  });
});

function getInitial() {
  return {
    opacity: 0,
    filter: `blur(${props.blur})`,
    y: props.yOffset,
  };
}

function getAnimate() {
  return {
    opacity: 1,
    filter: `blur(0px)`,
    y: 0,
  };
}
</script>

<!--<template>-->
<!--  <ClientOnly>-->
<!--    <BlurReveal-->
<!--      :delay="0.2"-->
<!--      :duration="0.75"-->
<!--      class="p-8"-->
<!--    >-->
<!--      <h2 class="text-3xl font-bold tracking-tighter xl:text-6xl/none sm:text-5xl">Hey there 👋</h2>-->
<!--      <span class="text-pretty text-xl tracking-tighter xl:text-4xl/none sm:text-3xl">-->
<!--        How is it going?-->
<!--      </span>-->
<!--    </BlurReveal>-->
<!--  </ClientOnly>-->
<!--</template>-->