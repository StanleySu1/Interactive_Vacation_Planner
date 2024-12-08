// Utility to create a websocket for sending/receiving chat data
export function sendPrompt(message, chunkListener) {
  let fullText = "";
  return new Promise((resolve, reject) => {
    // Assume our python server runs on localhost:8000
    const ws = new WebSocket("ws://localhost:8000/");
    // Send our prompt
    ws.addEventListener("open", (e) => {
      ws.send(JSON.stringify(message));
    });
    // Receiving messages...
    ws.addEventListener("message", (e) => {
      const msg = JSON.parse(e.data);
      if (msg.chunk) {
        fullText += msg.chunk;
        msg.fullText = fullText;
      }
      chunkListener(msg);
    });
    ws.addEventListener("close", (e) => {
      resolve(fullText);
    });
  });
}

