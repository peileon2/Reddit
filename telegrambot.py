from fastapi import FastAPI, BackgroundTasks
import os
import httpx
from dotenv import load_dotenv
import json

# 导入外部模块
# from Command.Qwen import qwen_plus_word
from Command.deepseekword import deepseek_word
from Resource.reddit import RedditScraper

app = FastAPI()

load_dotenv()  # 读取 .env 文件

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
client_id = os.getenv("Client_Id")
client_secret = os.getenv("Reddit_Secret")
user_agent = os.getenv("User_Agent")


class TelegramBot:
    def __init__(self, bot_token: str):
        self.bot_token = bot_token
        self.redditScraper = RedditScraper(
            client_id=client_id, client_secret=client_secret, user_agent=user_agent
        )

    async def send_message(self, chat_id: int, text: str):
        url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
        payload = {"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(url, json=payload)
                response.raise_for_status()  # 检查 HTTP 请求是否成功
            except httpx.HTTPStatusError as e:
                print(
                    f"Telegram API 错误: {e.response.status_code} - {e.response.text}"
                )
            except Exception as e:
                print(f"发送消息失败: {str(e)}")

    def json_to_markdown(self, data):
        # 创建 Markdown 内容
        markdown = f"**Spoken Version:** {data['spoken_version']}\n\n"
        markdown += "**Phrases Comparison:**\n"

        for phrase in data["phrases"]:
            original = phrase["original"]
            revised = phrase["revised"]
            # 无论是否改变，都将对比显示在列表中，并在每个对比后添加超链接
            markdown += f"- **Original**: {original}\n"
            markdown += f"  **Revised**: {revised}\n"
            markdown += f'  ["{original}" vs "{revised}"](https://www.deepseek.com/)\n\n'  # 添加超链接

        return markdown

    async def send_markdown(self, chat_id, text):
        ## tran json into markdown
        reply_json = deepseek_word.generate_analy_content(text)
        reply_markdwon = self.json_to_markdown(data=json.loads(reply_json))
        # print(reply_markdwon)
        await self.send_message(chat_id, reply_markdwon)

    async def handle_text_message(self, chat_id, text):
        post_text = self.redditScraper.fetch_and_format(subreddit_name="BBQ", limit=10)
        deepseek_word.generate_analy_content(keyword="", post_text=post_text)


# 创建 TelegramBot 实例
bot = TelegramBot(TELEGRAM_BOT_TOKEN)
