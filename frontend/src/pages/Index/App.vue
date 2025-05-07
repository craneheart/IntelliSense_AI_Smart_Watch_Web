<script setup>
import TopBar from '@/components/Sider/TopBar.vue';
import Footer from '@/components/Sider/Footer.vue'; // 导入页脚组件
import {initTheme} from '@/ulits/useTheme.js';

// 初始化主题
initTheme();
</script>

<template>
  <div id="app" class="h-full w-full flex flex-col">
    <!-- 顶部导航栏 -->
    <TopBar/>

    <!-- 主要内容区域 -->
    <main class="flex-grow">
      <!-- 路由视图 - 根据当前路由展示不同的页面组件 -->
      <router-view/>
    </main>

    <!-- 页脚 -->
    <Footer/>
  </div>
</template>

<style>
:root {
  --color-primary: #3298d7;
  --color-text: #313c3e;
  --color-background: #FFFFFF;
}

html, body {
  @apply h-full w-full font-sans;
  background-color: var(--color-background);
  color: var(--color-text);
}

#app {
  background-color: var(--color-background);
  color: var(--color-text);
}

.dark {
  --color-primary: #256295;
  --color-text: #ffffff;
  --color-background: #273d40;
}
</style>
