<script lang="ts" setup>
import {useTheme} from '@/ulits/useTheme.ts';
import {ref} from 'vue';
import RadianText from "@/components/text/RadianText.vue";

// 使用主题钩子
const {isDark, toggleTheme} = useTheme();

// 控制移动端菜单展开状态
const isMobileMenuOpen = ref(false);

// 导航菜单项
const navItems = [
  {name: '首页', path: '/'},
  {name: '智音助手', path: '/chat'},
  {name: '语音对话', path: '/voice'},
  {name: '文档展示', path: '/docs'},
];

// 切换移动菜单状态
const toggleMobileMenu = () => {
  isMobileMenuOpen.value = !isMobileMenuOpen.value;
};
</script>

<template>
  <header class="top-bar">
    <div class="container mx-auto px-4 py-4 flex justify-between items-center">
      <!-- Logo 和标题 -->
      <div class="flex items-center">
        <RadianText
            :duration="5"
            class="font-bold text-xl tracking-tight select-none cursor-pointer"
            @click="$router.replace('/')"
        >智音多模态AI手环
        </RadianText>
      </div>

      <!-- 桌面端导航 -->
      <nav class="hidden md:flex items-center space-x-8">
        <router-link
            v-for="item in navItems"
            :key="item.name"
            :to="item.path"
            class="nav-link py-1"
        >
          {{ item.name }}
        </router-link>
      </nav>

      <!-- 右侧功能区 -->
      <div class="flex items-center">
        <!-- 主题切换按钮 -->
        <button :title="isDark ? '切换到亮色模式' : '切换到暗色模式'" class="theme-toggle p-2 rounded-full"
                @click="toggleTheme">
          <!-- 根据当前主题显示不同图标 -->
          <svg v-if="isDark" class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"
               xmlns="http://www.w3.org/2000/svg">
            <path
                d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"
                stroke-linecap="round" stroke-linejoin="round"
                stroke-width="2"/>
          </svg>
          <svg v-else class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"
               xmlns="http://www.w3.org/2000/svg">
            <path d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"
                  stroke-linecap="round" stroke-linejoin="round"
                  stroke-width="2"/>
          </svg>
        </button>

        <!-- 移动端菜单按钮 -->
        <button class="md:hidden mobile-menu-button ml-4" @click="toggleMobileMenu">
          <svg class="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path d="M4 6h16M4 12h16M4 18h16" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"/>
          </svg>
        </button>
      </div>
    </div>

    <!-- 移动端菜单 -->
    <div v-if="isMobileMenuOpen" class="md:hidden mobile-menu">
      <div class="px-4 py-3 space-y-2">
        <router-link
            v-for="item in navItems"
            :key="item.name"
            :to="item.path"
            class="mobile-nav-link block py-3"
            @click="isMobileMenuOpen = false"
        >
          {{ item.name }}
        </router-link>
      </div>
    </div>
  </header>
</template>

<style scoped>
.top-bar {
  border-bottom: 1px solid rgba(125, 125, 125, 0.2);
  position: sticky;
  top: 0;
  z-index: 100;
  background-color: var(--color-background);
  backdrop-filter: blur(8px);
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.nav-link {
  position: relative;
  transition: all 0.3s ease;
  font-weight: 400;
}

.nav-link:hover,
.mobile-nav-link:hover {
  color: var(--color-text);
}

.nav-link.router-link-active {
  color: var(--color-primary);
  font-weight: 500;
}

.nav-link.router-link-active:after {
  content: "";
  position: absolute;
  bottom: -4px;
  left: 0;
  width: 100%;
  height: 2px;
  background-color: var(--color-primary);
  border-radius: 1px;
  transform: scaleX(1);
  transition: transform 0.3s ease;
}

.nav-link:not(.router-link-active):after {
  content: "";
  position: absolute;
  bottom: -4px;
  left: 0;
  width: 100%;
  height: 2px;
  background-color: var(--color-primary);
  border-radius: 1px;
  transform: scaleX(0);
  transition: transform 0.3s ease;
}

.nav-link:not(.router-link-active):hover:after {
  transform: scaleX(0.5);
}

.theme-toggle {
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--color-text);
}

.theme-toggle:hover {
  background-color: rgba(125, 125, 125, 0.1);
  transform: rotate(30deg);
}

.mobile-menu {
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  background-color: var(--color-background);
  border-bottom: 1px solid rgba(125, 125, 125, 0.2);
  animation: slideDown 0.3s ease-out;
}

.mobile-nav-link {
  transition: all 0.2s ease;
  border-radius: 6px;
  padding-left: 1rem;
}

.mobile-nav-link.router-link-active {
  color: var(--color-text);
  font-weight: 500;
  background-color: rgba(var(--color-text), 0.1);
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
