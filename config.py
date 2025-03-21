from openai import OpenAI


# QWEN_API_URL = "http://10.151.166.62:8000/v1"
# MODEL_NAME = "Qwen/Qwen2.5-0.5B-Instruct"
QWEN_API_URL = "http://103.237.29.236:10069/de_learning/v1"
MODEL_NAME = "Qwen/Qwen2.5-7B-Instruct"

client = OpenAI(base_url=QWEN_API_URL, api_key="none")

histories = [{
    "role": "system",
    "content": "你是一个专业的出行推荐官"
}]
