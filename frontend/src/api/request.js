import axios from 'axios';

const request = axios.create({
    baseURL: '/', // 与Django后端api路径匹配
    headers: {
        'Content-Type': 'application/json'
    },
    withCredentials: true // 确保跨域请求时携带cookies
});

// 添加请求拦截器处理CSRF令牌
request.interceptors.request.use(config => {
    // 获取CSRF令牌
    const csrfToken = getCookie('csrftoken');
    // 如果存在令牌且请求方法不是GET，则添加到请求头
    if (csrfToken && config.method && config.method.toLowerCase() !== 'get') {
        config.headers['X-CSRFToken'] = csrfToken;
    }

    return config;
});

// 辅助函数：从cookie中获取特定值
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
}

export default request;
