export default function connection(url) {
    const baseUrl = "ws://localhost:8000/ws";
    return new WebSocket(`${baseUrl}${url}`);
}