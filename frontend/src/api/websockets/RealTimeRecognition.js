import connection from "./router";

const url = "/voice/recognition/";

export function realTimeRecognition(onReadyCallback) {
    let isServerReady = false;
    const ws = connection(url);

    ws.onopen = async () => {
        ws.send(JSON.stringify({commend: 'signal', signal: 'init'}));
    }

    ws.onmessage = async (event) => {
        try {
            const data = JSON.parse(event.data);
            console.log(data)
            if (data.commend === "signal" && data.signal === "ready") {
                console.log(111)
                isServerReady = true;
                if (onReadyCallback) await onReadyCallback(data);
            }
        } catch (e) {
            console.error("解析WebSocket消息失败:", e);
        }
    };

    // 添加方法发送音频数据
    const sendAudioData = (audioData) => {
        if (ws && ws.readyState === WebSocket.OPEN && isServerReady) {
            ws.send(audioData);
        }
    };

    // 检查服务器是否准备好
    const isReady = () => isServerReady;

    // 关闭WebSocket连接
    const closeConnection = () => {
        if (ws && ws.readyState === WebSocket.OPEN) {
            ws.send(JSON.stringify({commend: 'signal', signal: 'close'}));
            // 不立即关闭，给服务器最后处理的时间
            setTimeout(() => {
                ws.close();
            }, 500);
        }
    };

    return {
        ws,
        sendAudioData,
        closeConnection,
        isReady
    };
}
