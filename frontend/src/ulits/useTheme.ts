import {ref, onMounted} from 'vue'

// 定义主题色配置
const themeColors = {
    light: {
        primary: '#3298d7',
        textColor: '#313c3e',
        backgroundColor: '#FFFFFF',
    },
    dark: {
        primary: '#bca5d5',
        textColor: '#dcd4e4',
        backgroundColor: '#000000',
    }
}


// 确定当前主题模式
function determineThemeMode() {
    const savedTheme = localStorage.getItem('theme')
    if (savedTheme === 'dark') return true
    if (savedTheme === 'light') return false
    return window.matchMedia('(prefers-color-scheme: dark)').matches
}

// 加载保存的主题色
function loadSavedThemeColor(isDark: boolean) {
    const themeMode = isDark ? 'dark' : 'light'
    const savedColor = localStorage.getItem(`primaryColor-${themeMode}`)

    if (savedColor) {
        themeColors[themeMode].primary = savedColor
    }

    return themeColors[themeMode].primary
}

// 应用主题到DOM
function applyTheme(isDark: boolean) {
    const theme = isDark ? themeColors.dark : themeColors.light

    // 应用CSS变量
    document.documentElement.style.setProperty('--color-primary', theme.primary)
    document.documentElement.style.setProperty('--color-text', theme.textColor)
    document.documentElement.style.setProperty('--color-background', theme.backgroundColor)

    // 直接设置背景色，确保立即生效
    document.body.style.backgroundColor = theme.backgroundColor
    document.body.style.color = theme.textColor

    // 更新dark类
    if (isDark) {
        document.documentElement.classList.add('dark')
    } else {
        document.documentElement.classList.remove('dark')
    }
}

// 初始化主题
export function initTheme() {
    const isDark = determineThemeMode()
    loadSavedThemeColor(isDark)
    applyTheme(isDark)
}

export function useTheme() {
    const isDark = ref(false)
    const primaryColor = ref('')

    // 更新主题和本地存储
    const updateTheme = () => {
        applyTheme(isDark.value)
        localStorage.setItem('theme', isDark.value ? 'dark' : 'light')
    }

    // 切换主题
    const toggleTheme = () => {
        isDark.value = !isDark.value
        primaryColor.value = loadSavedThemeColor(isDark.value)
        updateTheme()
    }

    // 设置主题色 - 优化版本
    const setPrimaryColor = (color: string) => {
        const themeMode = isDark.value ? 'dark' : 'light'

        // 更新颜色值
        primaryColor.value = color
        themeColors[themeMode].primary = color

        // 持久化存储
        localStorage.setItem(`primaryColor-${themeMode}`, color)

        // 立即应用更改
        applyTheme(isDark.value)
    }

    // 初始化
    onMounted(() => {

        // 确定主题模式并加载对应颜色
        isDark.value = determineThemeMode()
        primaryColor.value = loadSavedThemeColor(isDark.value)

        // 应用主题
        updateTheme()

        // 监听系统主题变化
        window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
            if (!localStorage.getItem('theme')) {
                isDark.value = e.matches
                primaryColor.value = loadSavedThemeColor(isDark.value)
                updateTheme()
            }
        })
    })

    return {
        isDark,
        toggleTheme,
        primaryColor,
        setPrimaryColor
    }
}

