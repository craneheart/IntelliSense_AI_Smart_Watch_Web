import {createRouter, createWebHashHistory} from 'vue-router'
import HomeView from "../views/HomeView.vue"

// 为MPA形式定义路由
// 在MPA中，每个页面都有自己的入口，路由主要用于页面内部导航
const routes = [
    {
        path: '/',
        name: 'home',
        component: HomeView,
        meta: {
            title: '首页',
        },
    },
    {
        path: '/chat',
        name: 'chat',
        component: () => import('../views/ChatView.vue'),
        meta: {
            title: '聊天',
        },
    },
    {
        path: '/voice',
        name: 'voice',
        component: () => import('../views/VoiceView.vue'),
        meta: {
            title: '语音',
        },
    },
    {
        path: '/docs',
        name: 'docs',
        component: () => import('../views/DocumentsView.vue'),
        meta: {
            title: '文档',
        },
    },
    {
        path: '/AI',
        name: 'AI模型',
        // component: () => import('../views/AIView.vue'),
    }
]

// 使用hash模式而不是history模式，避免服务器配置问题
const router = createRouter({
    history: createWebHashHistory(import.meta.env.BASE_URL),
    routes
})

export default router