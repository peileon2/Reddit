from openai import OpenAI
import os

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
if not DEEPSEEK_API_KEY:
    raise ValueError("DEEPSEEK_API_KEY 环境变量未设置！")


class DeepSeekWord:
    def __init__(self, model: str = "deepseek-chat"):
        # 初始化 DeepSeek 客户端
        self.client = OpenAI(
            api_key=DEEPSEEK_API_KEY, base_url="https://api.deepseek.com"
        )
        self.model = model  # 设置默认的模型名称

    def generate_analy_content(self, keyword, post_text):
        # System prompt - 描述AI助手的行为和任务
        message = {
            "role": "system",
            "content": (
                f'请判断以下Reddit帖子内容是否与“{keyword}”有关，如果相关返回 {{"related": true}}，否则返回 {{"related": false}}\n\n'
            ),
        }

        # User prompt - 动态地将输入句子插入
        user_message = {"role": "user", "content": f"{post_text}"}

        # Combine system and user prompts into messages list
        messages = [message, user_message]

        # 获取 DeepSeek 的回复
        response = self.client.chat.completions.create(
            model=self.model, messages=messages, response_format={"type": "json_object"}
        )

        # 打印True or False
        return response.choices[0].message.content


# 使用示例
deepseek_word = DeepSeekWord()
