import connection from "@/api/websockets/router.js";

export default function deepseek() {
    const url = "/computingUnit/deepseek/";
    const ws = connection(url);
    return {
        ws
    }
}