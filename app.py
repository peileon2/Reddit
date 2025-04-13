from fastapi import FastAPI, Request, HTTPException, BackgroundTasks
import os
import uvicorn
from dotenv import load_dotenv
from telegrambot import bot

app = FastAPI()

load_dotenv()  # 读取 .env 文件

SECRET_WEBHOOK_TOKEN = os.getenv("SECRET_WEBHOOK_TOKEN")


@app.post("/webhook")
async def telegram_webhook(request: Request, background_tasks: BackgroundTasks):
    # 获取请求头中的 Token
    secret_token = request.headers.get("X-Telegram-Bot-Api-Secret-Token")
    if secret_token != SECRET_WEBHOOK_TOKEN:
        # 调试信息：打印 `repr()` 来检查实际字符
        raise HTTPException(status_code=403, detail="Forbidden: Invalid secret token")

    # 解析 JSON 数据
    update = await request.json()

    if "message" in update:
        message = update["message"]
        chat_id = message["chat"]["id"]

        if "text" in message:
            reply_txt = await bot.handle_text_message(chat_id, message["text"])
            background_tasks.add_task(bot.send_markdown, chat_id, reply_txt)

    return {"ok": True}


# Cloud Run 需要监听 0.0.0.0:$PORT
if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))  # 默认 8080，但应确保 Cloud Run 传入了 PORT
    uvicorn.run(app, host="0.0.0.0", port=port)
