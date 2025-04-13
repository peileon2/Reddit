import requests
import os

SECRET_WEBHOOK_TOKEN = os.getenv("SECRET_WEBHOOK_TOKEN")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
# 替换为你的 Bot Token
bot_token = TELEGRAM_BOT_TOKEN

# 你的 Webhook URL
webhook_url = "https://deepseekapp-268195744076.us-west2.run.app/webhook"

# 如果你有 Secret Token，替换以下变量
secret_token = SECRET_WEBHOOK_TOKEN

# 设置 Webhook 请求的 URL
# 设置 Webhook 请求的 URL
url = f"https://api.telegram.org/bot{bot_token}/setWebhook?url={webhook_url}&secret_token={secret_token}"

# 发送 GET 请求来设置 Webhook
response = requests.get(url)


# 检查响应状态
if response.status_code == 200:
    print("Webhook set successfully!")
    print(response.json())
else:
    print(f"Failed to set webhook: {response.status_code}")
    print(response.text)
