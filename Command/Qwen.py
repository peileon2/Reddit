import os
from openai import OpenAI


# Set up the API client
class QwenPlusWord:
    def __init__(self, model: str = "qwen-plus"):
        # Initialize OpenAI client
        self.client = OpenAI(
            api_key=os.getenv("DASHSCOPE_API_KEY"),
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        )
        self.model = model  # Set the default model name

    def generate_text(self, content):
        # Prepare the messages with system instructions and user input
        messages = [
            {
                "role": "system",
                "content": """You are an English writing assistant. Your task is to correct the grammar of sentences while keeping the original words as much as possible. 

                1. **Grammar Errors**:
                - Correct any grammatical errors without changing the original vocabulary or word choices.

                2. **Output**:
                - Provide only the grammatically corrected sentence as a string, without any additional text, labels, or explanations.

                Example: 
                - Original: "I have a 朋友,I wanna go for a trip with 他."
                - Corrected: "I have a friend, I wanna go for a trip with him."
                """,
            },
            {"role": "user", "content": content},
        ]

        # Make the API call to the qwen-plus model
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
        )

        # Print and return the model's response
        print(response.choices[0].message.content)
        return response.choices[0].message.content


# Example usage
qwen_plus_word = QwenPlusWord()
# qwen_plus_word.generate_text("I donot know how i can 驱赶老鼠 in marry's 牧场")
