<script setup>
// 定义组件接收的属性
const props = defineProps({
  // 名字列表
  nameList: {
    type: Array,
    required: true
  },
  // 点击处理函数
  onClick: {
    type: Function,
    required: true
  }
});
</script>

<template>
  <div class="flex flex-col w-64 h-full bg-gray-100 shadow-md">
    <div class="flex flex-col p-4">
      <div
          v-for="(name, index) in nameList"
          :key="index"
          class="px-4 py-3 rounded-lg cursor-pointer text-gray-700 hover:bg-gray-200 hover:text-gray-900 transition-colors duration-200 mb-2"
          @click="onClick(name)"
      >
        {{ name }}
      </div>
    </div>
  </div>
</template>