export function base64(content, type) {
    const byteCharacters = atob(content);
    const byteNumbers = new Array(byteCharacters.length);

    for (let i = 0; i < byteCharacters.length; i++) {
        byteNumbers[i] = byteCharacters.charCodeAt(i) & 0xFF;
    }

    const byteArray = new Uint8Array(byteNumbers);
    const blob = new Blob([byteArray], {type: type});

    return URL.createObjectURL(blob);
}