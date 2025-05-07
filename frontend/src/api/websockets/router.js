export default function connection(url) {
    const baseUrl = "wss://crane.xyhrc.com/ws";
    return new WebSocket(`${baseUrl}${url}`);
}