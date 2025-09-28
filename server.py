from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Query
from deep_translator import GoogleTranslator
from fastapi.responses import FileResponse
from typing import Dict

app = FastAPI()

# ---------------- LANGUAGE MAP ----------------
LANGUAGE_MAP: Dict[str, str] = {
    "English": "en",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Japanese": "ja",
    "Korean": "ko",
    "Auto Detect": "auto"
}

# ---------------- TRANSLATION ----------------
async def translate_text_async(
    text: str,
    dest_lang_name: str,
    src_lang_name: str | None = None
) -> dict[str, str | None]:
    dest_lang_code = LANGUAGE_MAP.get(dest_lang_name, 'en')
    src_lang_code = LANGUAGE_MAP.get(src_lang_name, 'auto') if src_lang_name and src_lang_name != "Auto Detect" else 'auto'

    try:
        translated = GoogleTranslator(source=src_lang_code, target=dest_lang_code).translate(text)
        return {
            "success": "True",
            "translated_text": translated,
            "source_lang": src_lang_name or "Auto Detect",
            "error": None
        }
    except Exception as e:
        return {
            "success": "False",
            "translated_text": "Translation Failed",
            "source_lang": None,
            "error": str(e)
        }

# ---------------- CHAT MANAGER ----------------
class ConnectionManager:
    def __init__(self) -> None:
        self.active_connections: Dict[WebSocket, str] = {}

    async def connect(self, websocket: WebSocket, language: str) -> None:
        await websocket.accept()
        self.active_connections[websocket] = language

    def disconnect(self, websocket: WebSocket) -> None:
        self.active_connections.pop(websocket, None)

    async def broadcast(self, sender: WebSocket, message: str) -> None:
        sender_lang = self.active_connections.get(sender, "Auto Detect")
        for conn, lang in self.active_connections.items():
            if conn == sender:
                continue  # Don't send back to sender
            result = await translate_text_async(message, lang, src_lang_name=sender_lang)
            if result["success"] == "True":
                await conn.send_text(f"{sender_lang} → {lang}: {result['translated_text']}")
            else:
                await conn.send_text(f"[Error] {result['error']}")

manager = ConnectionManager()

# ---------------- WEBSOCKET ENDPOINT ----------------
@app.websocket("/ws/{lang}")
async def websocket_endpoint(websocket: WebSocket, lang: str) -> None:
    await manager.connect(websocket, lang)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(websocket, data)
    except WebSocketDisconnect:
        manager.disconnect(websocket)

# ---------------- TRANSLATE ENDPOINT ----------------
@app.get("/translate")
async def translate_endpoint(
    text: str = Query(...),
    dest: str = Query(...),
    src: str = Query("auto")
):
    result = await translate_text_async(text, dest_lang_name=dest, src_lang_name=src)
    return {"translated_text": result["translated_text"]}

# ---------------- SERVE FRONTEND ----------------
@app.get("/")
async def get_frontend() -> FileResponse:
    return FileResponse("index.html")

# ---------------- RUN SERVER ----------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
